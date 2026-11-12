"""
Times each stage of one FitFindr run, to find out which stage makes a run slow.

    python diagnose_latency.py --label before --runs 30

The log from runlog.py only has the total time per run. This script repeats the
same three steps as agent.py::run_agent, one at a time, with a timer around each:

    search    the MCP call to search_listings (starts its own Python process)
    outfit    the model call inside suggest_outfit
    card      the model call inside create_fit_card

It runs with the cache off, cycles through the five matching queries from
criteria.md, and waits between runs so the per-minute request limit in
generate.py is never reached. That way no stage time includes a rate-limit wait.

It does not change the system. Output: results/latency_diagnosis_<label>.md
"""

import argparse
import os
import statistics as st
import time

os.environ["AI201_CACHE"] = "0"          # must be set before config is imported

import config
from agent import parse_query
from mcp_client import call_tool
from tools import create_fit_card, suggest_outfit
from utils.data_loader import get_example_wardrobe

QUERIES = [
    "vintage graphic tee under $30",
    "90s track jacket in size M",
    "denim jacket under $50",
    "platform sneakers size 8",
    "silk slip dress in midi length under $40",
]
SECONDS_PER_RUN = 9      # 2 model calls per run, so at most about 13 calls a minute


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", default="before")
    parser.add_argument("--runs", type=int, default=30)
    args = parser.parse_args()

    wardrobe = get_example_wardrobe()
    rows = []
    for n in range(args.runs):
        query = QUERIES[n % len(QUERIES)]
        started = time.perf_counter()
        parsed = parse_query(query)

        t0 = time.perf_counter()
        results = call_tool("search_listings", {
            "description": parsed["description"],
            "size": parsed["size"],
            "max_price": parsed["max_price"],
        })
        t_search = time.perf_counter() - t0
        item = results[0]

        t0 = time.perf_counter()
        outfit = suggest_outfit(item, wardrobe)
        t_outfit = time.perf_counter() - t0

        t0 = time.perf_counter()
        create_fit_card(outfit, item)
        t_card = time.perf_counter() - t0

        total = time.perf_counter() - started
        rows.append((n + 1, query, t_search, t_outfit, t_card, total))
        print(f"run {n+1:>2}  search {t_search:5.2f}  outfit {t_outfit:5.2f}  "
              f"card {t_card:5.2f}  total {total:5.2f}  {query}", flush=True)
        time.sleep(max(0.0, SECONDS_PER_RUN - (time.perf_counter() - started)))

    write_report(rows, args.label)


def write_report(rows, label: str) -> None:
    def col(i):
        return [r[i] for r in rows]

    lines = [
        f"# Latency by stage ({label} the fix)", "",
        "- Produced by: `diagnose_latency.py::main`",
        f"- {len(rows)} runs, cache off, one run every {SECONDS_PER_RUN} seconds, five matching queries in turn",
        "- Times are seconds, measured around each stage with `time.perf_counter()`", "",
        "| Run | Query | search (MCP) | outfit (model) | card (model) | total |",
        "|---|---|---|---|---|---|",
    ]
    for n, q, a, b, c, total in rows:
        lines.append(f"| {n} | {q} | {a:.2f} | {b:.2f} | {c:.2f} | {total:.2f} |")

    lines += ["", "| Stage | Median | Lowest | Highest |", "|---|---|---|---|"]
    for name, i in (("search (MCP)", 2), ("outfit (model)", 3), ("card (model)", 4), ("total", 5)):
        v = col(i)
        lines.append(f"| {name} | {st.median(v):.2f} | {min(v):.2f} | {max(v):.2f} |")

    slow = [r for r in rows if r[5] > 5.0]
    lines += ["", f"Runs over 5.0 s: {len(slow)} of {len(rows)}.", ""]
    for n, q, a, b, c, total in slow:
        biggest = max((a, "search"), (b, "outfit"), (c, "card"))
        lines.append(f"- Run {n}: total {total:.2f} s, slowest stage was {biggest[1]} at {biggest[0]:.2f} s")
    path = config.RESULTS_DIR / f"latency_diagnosis_{label}.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nWrote {path}")


if __name__ == "__main__":
    main()
