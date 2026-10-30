# Coverage (step 2, light) — 2026-10-30
Notes: 15 fetched, 1 deprecated (2022 article), 1 is a geocode result (`search`), ~13 substantive. Min for light (10) met; target 15-25 not fully met.
Subagent hand-backs for batches 1 and 2 said only "placeholder"; notes were verified in the vault directly. Batch 3 gave a real report.
Tag caveat: fetchers tagged notes `cockburn-central-house-timing` (not the full vault_tag). Use that tag for lookups.

| Atomic item | Status | Evidence | Gap |
|---|---|---|---|
| Address anchor | Adequate | REIWA sold record 11 Furlong; Nominatim resolves STREET only (-32.1158872, 115.8494353), not house number | 1 km radius not computed with point-level coordinates |
| Item1 price change | Thin | REIWA suburb profile (12m to Sep 2026 house median $975,000, +21.7%); nearby sold records (27 Furlong 29 Jan 2026 $940k; 27 Paddock 22 May 2026 $1.0m; 11 Furlong 13 May 2025 $768k) | prior comparable annual period for suburb not obtained; no 1 km house sample set; property types mixed (townhouse-type small lots) |
| Item2 inventory change | Thin / mostly missing | single-time snapshot only (REIWA for-sale page: inconsistent 210 vs 268, surrounding suburbs, all types); Perth metro active listings 5,137 (May 2026) | no same-scope two-time series -> change = missing at suburb/1km |
| Item3 negative equity | n/a research | pure arithmetic in step 10 | — |
| Support/oppose context | Adequate | REIWA Oct 2026 quarterly, Australian Broker, ANZ via API Mag, REIWA forecast | RBA/Cotality primary data not fetched |
Blocked: microburbs.com.au (bot_block, queued escalation #1). Not drained: browser lane not run (cost/low value; no CAPTCHA handoff needed); recorded as unfetched.
Retraction check: n/a (no DOIs; sources score scored 0).
claims ingest error: claims-perth-property-price-growth-slowed-... JSON unreadable (invalid escape); the note body itself is intact.
