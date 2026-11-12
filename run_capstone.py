"""
Runs the five capstone criteria from criteria.md against the real server.

    python run_capstone.py --label before --runs 3

One "run" is the whole test, once: five trials for each of the five criteria,
scored exactly as criteria.md words them. The script starts the servers itself,
sends every request over HTTP, and reads the log line each request wrote.
Nothing about the system changes between runs, and the cache is off.

Servers it starts (each as `python serve.py`, with AI201_CACHE=0):
    A  real key, port 5000   warm-up, criteria 1, 2, 4 and 5
    C  real key, port 5001   criterion 3 (four of its five requests)
    B  FAKE key, port 5002   criterion 3 (the wrong-key request)

Criteria 1, 4 and 5 are scored from the same five matching requests: the
response is checked for criterion 1, and the log line it wrote is checked for
latency (criterion 4) and tokens (criterion 5).

Output: results/capstone_<label>.md, with the table and the raw log lines.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime

import config

LOG = config.ROOT / "logs" / "runs.jsonl"

MATCHING = [
    "vintage graphic tee under $30",
    "90s track jacket in size M",
    "denim jacket under $50",
    "platform sneakers size 8",
    "silk slip dress in midi length under $40",
]
IMPOSSIBLE = "designer ballgown size XXS under $5"
FIELDS = ["timestamp", "query", "outcome", "output", "selected_item_id",
          "latency_s", "model_calls", "cache_hits", "prompt_tokens", "output_tokens"]

PAUSE_BETWEEN_SERVERS = 30   # seconds, so the model service's per-minute limit is not hit
PAUSE_BETWEEN_RUNS = 60


# ── helpers ───────────────────────────────────────────────────────────────────

def log_lines() -> list[str]:
    return LOG.read_text(encoding="utf-8").splitlines() if LOG.exists() else []


class Server:
    """Start `python serve.py` on a port, wait until /health answers, stop it after."""

    def __init__(self, port: int, fake_key: bool = False):
        self.port = port
        self.env = dict(os.environ, AI201_CACHE="0", PORT=str(port))
        if fake_key:
            self.env["GEMINI_API_KEY"] = "not-a-real-key"
        self.err = tempfile.NamedTemporaryFile("w+", suffix=".txt", delete=False)

    def __enter__(self):
        self.proc = subprocess.Popen(
            [sys.executable, "serve.py"], cwd=config.ROOT, env=self.env,
            stdout=subprocess.DEVNULL, stderr=self.err,
        )
        for _ in range(60):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{self.port}/health", timeout=2).read()
                return self
            except OSError:
                time.sleep(0.5)
        raise SystemExit(f"Server on port {self.port} did not start.")

    def __exit__(self, *exc):
        self.proc.terminate()
        self.proc.wait(timeout=15)
        self.err.flush()

    def rate_limit_pauses(self) -> int:
        self.err.flush()
        with open(self.err.name, encoding="utf-8", errors="replace") as f:
            return f.read().count("[rate limit]")


def send(port: int, query: str) -> dict:
    """POST one query. Returns the status, the response body, and the new log line(s)."""
    before = len(log_lines())
    request = urllib.request.Request(
        f"http://127.0.0.1:{port}/ask",
        data=json.dumps({"query": query}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            status, body = response.status, json.load(response)
    except urllib.error.HTTPError as err:
        status, body = err.code, json.load(err)
    new = log_lines()[before:]
    line = None
    try:
        line = json.loads(new[-1]) if new else None
    except json.JSONDecodeError:
        pass
    return {"query": query, "status": status, "body": body,
            "n_new": len(new), "raw": new[-1] if new else None, "line": line}


def nonblank(value) -> bool:
    return isinstance(value, str) and value.strip() != ""


# ── scoring: one function per criterion, worded like criteria.md ──────────────

def score_1(t) -> bool:
    return (t["status"] == 200 and t["body"].get("error") is None
            and nonblank(t["body"].get("fit_card")))


def score_2(t) -> bool:
    error = t["body"].get("error") or ""
    line = t["line"] or {}
    return (t["status"] == 200 and t["body"].get("fit_card") is None
            and re.search(r"price|size|keyword", error, re.I) is not None
            and t["n_new"] == 1 and line.get("outcome") == "no_results"
            and line.get("model_calls") == 0)


def score_3(t, expected: str) -> bool:
    line = t["line"]
    if t["n_new"] != 1 or line is None:
        return False
    if any(f not in line for f in FIELDS):
        return False
    if line["outcome"] != expected:
        return False
    if not (nonblank(line["timestamp"]) and nonblank(line["outcome"]) and nonblank(line["output"])):
        return False
    numbers = ["latency_s", "model_calls", "cache_hits", "prompt_tokens", "output_tokens"]
    if not all(isinstance(line[k], (int, float)) and not isinstance(line[k], bool) for k in numbers):
        return False
    if expected != "rejected" and not nonblank(line["query"]):
        return False
    if expected not in ("rejected", "no_results") and line["selected_item_id"] is None:
        return False
    return True


def score_4(t) -> bool:
    line = t["line"]
    return t["n_new"] == 1 and line is not None and line["latency_s"] <= 5.0


def score_5(t) -> bool:
    line = t["line"]
    return (t["n_new"] == 1 and line is not None
            and line["prompt_tokens"] + line["output_tokens"] <= 600
            and line["model_calls"] == 2)


# ── one full run ──────────────────────────────────────────────────────────────

def one_run(run_number: int) -> dict:
    print(f"\n===== run {run_number} =====", flush=True)
    result = {"c1": [], "c2": [], "c3": [], "c4": [], "c5": [], "notes": []}

    with Server(5000) as a:
        send(a.port, MATCHING[0])                      # warm-up, not counted
        for q in MATCHING:
            t = send(a.port, q)
            result["c1"].append((t, score_1(t)))
            result["c4"].append((t, score_4(t)))
            result["c5"].append((t, score_5(t)))
            print(f"  match   {q[:40]:<40} c1={score_1(t)} c4={score_4(t)} c5={score_5(t)}", flush=True)
        for _ in range(5):
            t = send(a.port, IMPOSSIBLE)
            result["c2"].append((t, score_2(t)))
            print(f"  nomatch {IMPOSSIBLE[:40]:<40} c2={score_2(t)}", flush=True)
        pauses = a.rate_limit_pauses()
    result["notes"].append(f"server A rate-limit pauses: {pauses}")
    time.sleep(PAUSE_BETWEEN_SERVERS)

    plan = [(MATCHING[0], "ok"), (MATCHING[1], "ok"), (IMPOSSIBLE, "no_results"), ("", "rejected")]
    with Server(5001) as c:
        for q, expected in plan:
            t = send(c.port, q)
            result["c3"].append((t, score_3(t, expected), expected))
            print(f"  c3 {expected:<18} {q[:30]!r:<34} pass={score_3(t, expected)}", flush=True)
        pauses = c.rate_limit_pauses()
    result["notes"].append(f"server C rate-limit pauses: {pauses}")
    with Server(5002, fake_key=True) as b:
        t = send(b.port, MATCHING[0])
        result["c3"].append((t, score_3(t, "model_unavailable"), "model_unavailable"))
        print(f"  c3 {'model_unavailable':<18} {MATCHING[0][:30]!r:<34} pass={score_3(t, 'model_unavailable')}", flush=True)
    return result


def tally(trials, index=1) -> int:
    return sum(1 for t in trials if t[index])


# ── writing the results file ──────────────────────────────────────────────────

TARGETS = [
    ("1. A matching query completes", "at least 4 of 5", "c1", 4),
    ("2. An impossible query stops before any model call", "5 of 5", "c2", 5),
    ("3. Every kind of request leaves one complete log line", "5 of 5", "c3", 5),
    ("4. A warm matching request takes 5.0 s or less", "at least 4 of 5", "c4", 4),
    ("5. One matching run uses 600 tokens or fewer", "5 of 5", "c5", 5),
]


def write_results(label: str, runs: list[dict]) -> None:
    out = [f"# Capstone run log: {label}", "",
           f"- Produced by: `run_capstone.py` (`one_run`), scoring as worded in `criteria.md`",
           f"- Servers: `serve.py` with the cache off; `logs/runs.jsonl` is written by `runlog.py::run_logged`",
           f"- When: {datetime.now():%Y-%m-%d %H:%M}",
           f"- Runs: {len(runs)}, with the whole test repeated each time and nothing changed in between", ""]
    out += ["| Criterion | Target | " + " | ".join(f"Run {i+1}" for i in range(len(runs))) + " | Verdict |",
            "|---|---|" + "---|" * len(runs) + "---|"]
    for name, target, key, need in TARGETS:
        counts = [tally(r[key]) for r in runs]
        verdict = "MET" if all(c >= need for c in counts) else "MISSED"
        out.append(f"| {name} | {target} | " + " | ".join(f"{c}/5" for c in counts) + f" | {verdict} |")
    out += ["", "A criterion is MET only if every run reaches its target.", ""]
    for i, r in enumerate(runs, 1):
        out += [f"## Run {i}", "", *[f"- {n}" for n in r["notes"]], ""]
        for name, _, key, _ in TARGETS:
            out += [f"### {name}", ""]
            for item in r[key]:
                t, ok = item[0], item[1]
                extra = f" (expected `{item[2]}`)" if key == "c3" else ""
                out.append(f"- {'PASS' if ok else 'FAIL'}{extra}: `{t['query']}` -> HTTP {t['status']}, "
                           f"{t['n_new']} new log line(s)")
            out += ["", "Log lines written:", "", "```json"]
            out += [item[0]["raw"] or "(no log line)" for item in r[key]]
            out += ["```", ""]
    path = config.RESULTS_DIR / f"capstone_{label}.md"
    path.write_text("\n".join(out), encoding="utf-8")
    print(f"\nWrote {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    parser.add_argument("--runs", type=int, default=3)
    args = parser.parse_args()

    runs = []
    for i in range(1, args.runs + 1):
        runs.append(one_run(i))
        if i < args.runs:
            print(f"\n(waiting {PAUSE_BETWEEN_RUNS}s before the next run)", flush=True)
            time.sleep(PAUSE_BETWEEN_RUNS)
    write_results(args.label, runs)


if __name__ == "__main__":
    main()
