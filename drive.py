"""
Send a set of queries to a running FitFindr server, so the log fills up.

    python serve.py          (in one terminal)
    python drive.py          (in a second terminal)

Each request goes over HTTP to POST /ask, the same way any other client would.
The server writes the log (logs/runs.jsonl); this script only prints a short
line per request so progress is visible.

Options:
    python drive.py --port 5000     the port the server is on (default 5000)
    python drive.py --rounds 2      send the whole list this many times
"""

import argparse
import json
import time
import urllib.error
import urllib.request

# Six queries the data can match, one it cannot.
QUERIES = [
    "vintage graphic tee under $30",
    "90s track jacket in size M",
    "silk slip dress in midi length under $40",
    "platform sneakers size 8",
    "denim jacket under $50",
    "cargo pants under $30",
    "designer ballgown size XXS under $5",
]


def ask(base: str, query: str) -> tuple[int, dict]:
    """POST one query. Returns (HTTP status, response body as a dict)."""
    request = urllib.request.Request(
        f"{base}/ask",
        data=json.dumps({"query": query}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as err:
        return err.code, json.load(err)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--rounds", type=int, default=1)
    args = parser.parse_args()
    base = f"http://localhost:{args.port}"

    try:
        urllib.request.urlopen(f"{base}/health", timeout=10).read()
    except OSError:
        raise SystemExit(f"No server at {base}. Start it first with: python serve.py")

    for round_number in range(1, args.rounds + 1):
        for query in QUERIES:
            start = time.perf_counter()
            status, body = ask(base, query)
            took = time.perf_counter() - start
            result = "error: " + body["error"][:50] if body.get("error") else "fit card"
            print(f"[{round_number}] HTTP {status}  {took:5.1f}s  {result:<60}  {query}")


if __name__ == "__main__":
    main()
