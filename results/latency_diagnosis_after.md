# Latency by stage (after the fix)

- Produced by: `diagnose_latency.py::main`
- 30 runs, cache off, one run every 9 seconds, five matching queries in turn
- Times are seconds, measured around each stage with `time.perf_counter()`

| Run | Query | search (MCP) | outfit (model) | card (model) | total |
|---|---|---|---|---|---|
| 1 | vintage graphic tee under $30 | 2.48 | 2.18 | 0.80 | 5.45 |
| 2 | 90s track jacket in size M | 1.01 | 1.69 | 0.72 | 3.43 |
| 3 | denim jacket under $50 | 0.90 | 1.16 | 0.83 | 2.89 |
| 4 | platform sneakers size 8 | 0.85 | 0.59 | 0.60 | 2.04 |
| 5 | silk slip dress in midi length under $40 | 0.93 | 0.54 | 0.98 | 2.45 |
| 6 | vintage graphic tee under $30 | 0.85 | 0.48 | 0.65 | 1.98 |
| 7 | 90s track jacket in size M | 0.90 | 0.72 | 0.66 | 2.29 |
| 8 | denim jacket under $50 | 0.83 | 0.79 | 0.65 | 2.26 |
| 9 | platform sneakers size 8 | 0.83 | 0.90 | 0.55 | 2.28 |
| 10 | silk slip dress in midi length under $40 | 0.86 | 0.58 | 0.68 | 2.12 |
| 11 | vintage graphic tee under $30 | 0.84 | 0.56 | 0.64 | 2.04 |
| 12 | 90s track jacket in size M | 0.83 | 0.80 | 0.60 | 2.23 |
| 13 | denim jacket under $50 | 0.86 | 0.63 | 0.60 | 2.10 |
| 14 | platform sneakers size 8 | 0.86 | 0.64 | 0.67 | 2.17 |
| 15 | silk slip dress in midi length under $40 | 0.84 | 0.59 | 0.49 | 1.91 |
| 16 | vintage graphic tee under $30 | 0.84 | 0.64 | 1.29 | 2.76 |
| 17 | 90s track jacket in size M | 0.85 | 0.90 | 0.69 | 2.44 |
| 18 | denim jacket under $50 | 0.84 | 0.64 | 0.60 | 2.08 |
| 19 | platform sneakers size 8 | 0.84 | 0.66 | 0.75 | 2.25 |
| 20 | silk slip dress in midi length under $40 | 0.84 | 0.73 | 1.08 | 2.65 |
| 21 | vintage graphic tee under $30 | 0.84 | 0.82 | 0.64 | 2.30 |
| 22 | 90s track jacket in size M | 0.84 | 0.60 | 0.60 | 2.03 |
| 23 | denim jacket under $50 | 0.92 | 0.99 | 0.65 | 2.56 |
| 24 | platform sneakers size 8 | 0.87 | 0.58 | 0.65 | 2.10 |
| 25 | silk slip dress in midi length under $40 | 0.84 | 0.64 | 0.75 | 2.23 |
| 26 | vintage graphic tee under $30 | 0.82 | 0.59 | 0.93 | 2.34 |
| 27 | 90s track jacket in size M | 0.82 | 0.88 | 0.76 | 2.46 |
| 28 | denim jacket under $50 | 0.84 | 0.79 | 0.67 | 2.30 |
| 29 | platform sneakers size 8 | 0.83 | 0.64 | 0.69 | 2.16 |
| 30 | silk slip dress in midi length under $40 | 1.05 | 0.87 | 1.08 | 3.01 |

| Stage | Median | Lowest | Highest |
|---|---|---|---|
| search (MCP) | 0.84 | 0.82 | 2.48 |
| outfit (model) | 0.65 | 0.48 | 2.18 |
| card (model) | 0.67 | 0.49 | 1.29 |
| total | 2.27 | 1.91 | 5.45 |

Runs over 5.0 s: 1 of 30.

- Run 1: total 5.45 s, slowest stage was search at 2.48 s
