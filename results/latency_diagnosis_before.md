# Latency by stage (before the fix)

- Produced by: `diagnose_latency.py::main`
- 30 runs, cache off, one run every 9 seconds, five matching queries in turn
- Times are seconds, measured around each stage with `time.perf_counter()`

| Run | Query | search (MCP) | outfit (model) | card (model) | total |
|---|---|---|---|---|---|
| 1 | vintage graphic tee under $30 | 4.42 | 3.15 | 0.67 | 8.25 |
| 2 | 90s track jacket in size M | 1.49 | 0.62 | 0.65 | 2.76 |
| 3 | denim jacket under $50 | 1.72 | 0.74 | 1.21 | 3.68 |
| 4 | platform sneakers size 8 | 1.50 | 0.81 | 0.66 | 2.97 |
| 5 | silk slip dress in midi length under $40 | 1.55 | 0.57 | 0.73 | 2.85 |
| 6 | vintage graphic tee under $30 | 1.43 | 0.72 | 0.64 | 2.79 |
| 7 | 90s track jacket in size M | 1.21 | 0.80 | 0.87 | 2.88 |
| 8 | denim jacket under $50 | 1.86 | 0.75 | 1.87 | 4.48 |
| 9 | platform sneakers size 8 | 1.84 | 1.10 | 1.13 | 4.06 |
| 10 | silk slip dress in midi length under $40 | 4.98 | 0.75 | 0.74 | 6.46 |
| 11 | vintage graphic tee under $30 | 1.96 | 0.74 | 0.76 | 3.46 |
| 12 | 90s track jacket in size M | 1.46 | 9.44 | 0.61 | 11.52 |
| 13 | denim jacket under $50 | 1.34 | 0.84 | 0.90 | 3.08 |
| 14 | platform sneakers size 8 | 1.29 | 0.54 | 0.70 | 2.53 |
| 15 | silk slip dress in midi length under $40 | 1.21 | 0.69 | 0.74 | 2.64 |
| 16 | vintage graphic tee under $30 | 1.26 | 0.89 | 0.72 | 2.88 |
| 17 | 90s track jacket in size M | 1.34 | 0.57 | 0.57 | 2.48 |
| 18 | denim jacket under $50 | 1.45 | 0.66 | 8.90 | 11.00 |
| 19 | platform sneakers size 8 | 2.33 | 0.55 | 0.67 | 3.54 |
| 20 | silk slip dress in midi length under $40 | 1.29 | 0.78 | 0.93 | 3.00 |
| 21 | vintage graphic tee under $30 | 1.30 | 1.78 | 0.74 | 3.83 |
| 22 | 90s track jacket in size M | 1.24 | 0.78 | 0.66 | 2.67 |
| 23 | denim jacket under $50 | 1.19 | 9.07 | 0.69 | 10.96 |
| 24 | platform sneakers size 8 | 1.29 | 0.65 | 2.68 | 4.63 |
| 25 | silk slip dress in midi length under $40 | 1.46 | 0.96 | 0.81 | 3.23 |
| 26 | vintage graphic tee under $30 | 1.30 | 0.67 | 0.75 | 2.73 |
| 27 | 90s track jacket in size M | 1.27 | 0.83 | 0.56 | 2.67 |
| 28 | denim jacket under $50 | 1.25 | 0.74 | 0.72 | 2.70 |
| 29 | platform sneakers size 8 | 1.19 | 8.21 | 0.57 | 9.97 |
| 30 | silk slip dress in midi length under $40 | 2.05 | 1.01 | 0.64 | 3.70 |

| Stage | Median | Lowest | Highest |
|---|---|---|---|
| search (MCP) | 1.39 | 1.19 | 4.98 |
| outfit (model) | 0.76 | 0.54 | 9.44 |
| card (model) | 0.73 | 0.56 | 8.90 |
| total | 3.15 | 2.48 | 11.52 |

Runs over 5.0 s: 6 of 30.

- Run 1: total 8.25 s, slowest stage was search at 4.42 s
- Run 10: total 6.46 s, slowest stage was search at 4.98 s
- Run 12: total 11.52 s, slowest stage was outfit at 9.44 s
- Run 18: total 11.00 s, slowest stage was card at 8.90 s
- Run 23: total 10.96 s, slowest stage was outfit at 9.07 s
- Run 29: total 9.97 s, slowest stage was outfit at 8.21 s
