"""
Structured run log: one JSON line per request, written to logs/runs.jsonl.

run_logged() wraps run_agent(). It does not change what the agent does. It
times the run, counts the model calls and tokens the run used, and appends
one record. It is called from serve.py, which only runs one request at a time,
so the call and token counts it reads from generate.py belong to this run.

Fields in each line:
    timestamp        when the request finished (UTC, ISO format)
    query            what the user typed
    outcome          ok | no_results | model_unavailable | exception
    output           the fit card if the run worked, otherwise the error text
    selected_item_id the listing the agent picked, or null
    latency_s        seconds from start to finish, including the MCP search
    model_calls      requests sent to the model during this run
    cache_hits       answers reused from the cache (a cached run costs 0 tokens)
    prompt_tokens    tokens sent to the model, as reported by the service
    output_tokens    tokens the model wrote back, as reported by the service

Read the log back with:  python runlog.py
"""

import json
import time
from datetime import datetime, timezone

import config
import generate
from agent import run_agent

LOG_PATH = config.ROOT / "logs" / "runs.jsonl"


def _outcome(session: dict) -> str:
    """Name what happened, from the finished session."""
    if not session["error"]:
        return "ok"
    # The loop only sets an error after a successful search when the model
    # could not be reached, so an error with no search results is the empty branch.
    if not session["search_results"]:
        return "no_results"
    return "model_unavailable"


def _write(record: dict) -> None:
    LOG_PATH.parent.mkdir(exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def run_logged(query: str, wardrobe: dict) -> dict:
    """Run the agent once, log the run, and return the session unchanged."""
    tokens_before = generate.token_counts()
    calls_before = generate.call_count()
    hits_before = generate._cache_hits
    start = time.perf_counter()

    session = None
    failure = None
    try:
        session = run_agent(query, wardrobe)
    except Exception as exc:  # noqa: BLE001 - logged, then raised again below
        failure = f"{type(exc).__name__}: {exc}"

    tokens_after = generate.token_counts()
    if failure:
        outcome, output, item_id = "exception", failure, None
    else:
        outcome = _outcome(session)
        output = session["fit_card"] if outcome == "ok" else session["error"]
        item_id = (session["selected_item"] or {}).get("id")

    _write({
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "query": query,
        "outcome": outcome,
        "output": output,
        "selected_item_id": item_id,
        "latency_s": round(time.perf_counter() - start, 2),
        "model_calls": generate.call_count() - calls_before,
        "cache_hits": generate._cache_hits - hits_before,
        "prompt_tokens": tokens_after["prompt"] - tokens_before["prompt"],
        "output_tokens": tokens_after["output"] - tokens_before["output"],
    })

    if failure:
        # Same behaviour as before logging existed: the caller sees the error.
        raise RuntimeError(failure)
    return session


def show_log() -> None:
    """Print the log as a short table."""
    if not LOG_PATH.exists():
        print("No log yet. Start the server and send it a request first.")
        return
    print(f"{'time (UTC)':<20} {'outcome':<18} {'secs':>6} {'tokens':>7}  query")
    for line in LOG_PATH.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        tokens = r["prompt_tokens"] + r["output_tokens"]
        print(f"{r['timestamp'][:19]:<20} {r['outcome']:<18} {r['latency_s']:>6} "
              f"{tokens:>7}  {r['query']}")


if __name__ == "__main__":
    show_log()
