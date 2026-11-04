"""Export explicitly selected run artifacts; never modify originals or read keys.

The public trace preserves every event, but read_frozen source bodies are
replaced with length/hash metadata. Full requests/responses stay local; their
hashes and existence are listed so an export is not mistaken for a full replay.
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = (
    'deepseek-flash-01', 'my-run-20261101-144909',
    'audit-retry-20261101-152426', 'repaired-run-20261104-180813',
    'furlong-2km-run-20261104-184811', 'furlong-2km-fixed-20261104-190259',
)
PUBLIC_FILES = {
    'run.json', 'protocol.json', 'plan.json', 'claims.json', 'gaps.json',
    'report.md', 'report-audit.json', 'trace.jsonl', 'quality-review.md',
    'comparison.md', 'comparison-metrics.json', 'artifact-check.json',
    '09-report_audit-error.json', 'deferred-claims.json',
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def sanitize(text):
    # Remove local account paths from COPIES. Preserve URLs and research facts.
    text = re.sub(r'/'+r'Users/[^/\s"<>]+', '<LOCAL_HOME>', text)
    patterns = (r'sk-[A-Za-z0-9_-]{20,}',
                r'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})',
                r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY')
    if any(re.search(p, text) for p in patterns):
        raise ValueError('Potential credential in selected export; manual review required')
    return text

def public_trace(text):
    rows = []
    for line in text.splitlines():
        event = json.loads(line)
        data = event.get('data', {})
        if event.get('event') == 'tool' and data.get('name') == 'read_frozen':
            for source in data.get('observation', []):
                if 'text' in source:
                    body = source.pop('text')
                    source['public_export_body'] = {
                        'omitted': True, 'utf8_bytes': len(body.encode('utf-8')),
                        'sha256': sha(body.encode('utf-8')),
                        'reason': 'Full frozen source bodies remain local',
                    }
        rows.append(json.dumps(event, ensure_ascii=False))
    return '\n'.join(rows)+'\n'

def main():
    target = ROOT/'evidence/live-runs'
    target.mkdir(parents=True, exist_ok=True)
    manifest = {'policy': 'Selected artifacts; home paths redacted; all trace events retained; read_frozen bodies replaced by hashes. Original local files unchanged.',
                'not_a_complete_raw_api_or_corpus_export': True, 'runs': []}
    for name in RUNS:
        source = ROOT/'.local-runs'/name
        if not (source/'run.json').is_file():
            raise ValueError('Missing expected historical run: '+name)
        dest = target/name
        dest.mkdir(exist_ok=True)
        entry = {'name': name, 'files': [], 'local_only_files': []}
        for file in sorted(source.iterdir()):
            if not file.is_file():
                continue
            raw = file.read_bytes()
            if file.name not in PUBLIC_FILES:
                # Do not publish arbitrary files even if added to a run later.
                entry['local_only_files'].append({'name': file.name, 'sha256': sha(raw), 'bytes': len(raw)})
                continue
            text = raw.decode('utf-8')
            if file.name == 'trace.jsonl': text = public_trace(text)
            if file.name == 'quality-review.md':
                # The review was authored beside local docs. Relocate its known
                # guide link in the public copy only; the manifest records it.
                text = text.replace('](live-run.md)', '](../../../docs/live-run.md)')
            exported = sanitize(text).encode('utf-8')
            (dest/file.name).write_bytes(exported)
            entry['files'].append({'name': file.name, 'original_sha256': sha(raw),
                                   'exported_sha256': sha(exported),
                                   'transformed': raw != exported})
            if file.read_bytes() != raw:
                raise ValueError('Source changed during export: '+file.name)
        state = json.loads((source/'run.json').read_text())
        entry['status'] = state['status']
        entry['estimated_cost_cny'] = state.get('estimated_cost_cny')
        manifest['runs'].append(entry)
    (target/'export-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'exported_runs':len(manifest['runs']),
                      'exported_files':sum(len(r['files']) for r in manifest['runs'])}))

if __name__=='__main__': main()
