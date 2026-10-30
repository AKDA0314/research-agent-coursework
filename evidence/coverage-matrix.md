## Coverage Matrix — query phrase → atomic item mapping

| Query phrase (verbatim) | Mapped atomic item(s) | Scope check | Gap? |
|---|---|---|---|
| "Cockburn Central" | address anchor; suburb background | OK | No |
| "house" | scope_conditions: house only | OK | No |
| "现在买入" | cutoff 2026-10-30; supporting/opposing | OK | No |
| "支持证据、反对证据" | sub_q 1,2; heading 3 | OK | No |
| "还缺什么" | sub_q 3; gaps | OK | No |
| "11 furlong st ... 附近" | sub_q 4; 1 km radius | OK | No |
| 事项1 价格变化 | sub_q 5 | OK | No |
| 事项2 在售库存 | sub_q 6 | OK | No |
| 事项3 负资产 | sub_q 7 | OK | No |
