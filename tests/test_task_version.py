import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from six_step import digest,dump

class TaskVersionTests(unittest.TestCase):
    def test_check_accepts_explicit_new_task_but_rejects_tampering_without_api(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp); f=p/'frozen'; f.mkdir(); t=p/'task.md'
            t.write_text('New scope 2km');(f/'task.md').write_bytes(t.read_bytes())
            dump(f/'corpus.json',[{'source_id':'d','text':'source','body_sha256':digest(b'source')}])
            dump(f/'manifest.json',{'task_sha256':digest(t.read_bytes()),'corpus_sha256':digest((f/'corpus.json').read_bytes())})
            cmd=[sys.executable,str(ROOT/'scripts/run_live.py'),'check','--task',str(t),'--frozen',str(f)]
            good=subprocess.run(cmd,capture_output=True,text=True)
            self.assertEqual(good.returncode,0,good.stderr)
            self.assertEqual(json.loads(good.stdout)['api_calls'],0)
            self.assertFalse(json.loads(good.stdout)['same_task_as_original'])
            t.write_text('Changed after freeze')
            bad=subprocess.run(cmd,capture_output=True,text=True)
            self.assertNotEqual(bad.returncode,0)
            self.assertIn('differs from --task',bad.stderr)

if __name__=='__main__':unittest.main()
