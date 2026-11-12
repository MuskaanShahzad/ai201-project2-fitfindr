"""
Checks the model timeout in generate.py by forcing a stall.

    python check_timeout.py

In the timed runs, a model call sometimes took 8 to 9 s instead of 0.7 s
(results/latency_diagnosis_before.md). Real stalls are random, so this script
makes one on purpose: the first model call sleeps for 9 s, then every later call
is real. It makes the same request twice:

    with the timeout      config.MODEL_TIMEOUT_S as set in config.py (2 s)
    without the timeout   MODEL_TIMEOUT_S raised to 30 s, so the stall is waited out

and prints how long each took and how many model calls were made.
"""

import os
import time

os.environ["AI201_CACHE"] = "0"

import config
import generate

STALL_SECONDS = 9


class StallOnce:
    """Wraps the real client. Its first generate_content call hangs, the rest are real."""

    def __init__(self, client):
        self.client = client
        self.stalled = False

    @property
    def models(self):
        return self

    def generate_content(self, **kwargs):
        if not self.stalled:
            self.stalled = True
            time.sleep(STALL_SECONDS)
        return self.client.models.generate_content(**kwargs)


def one_request(label: str, timeout_s: float) -> None:
    config.MODEL_TIMEOUT_S = timeout_s
    generate._client = StallOnce(real_client)
    calls_before = generate.call_count()
    start = time.perf_counter()
    text = generate.generate("Say hello in five words.", cache=False)
    took = time.perf_counter() - start
    print(f"{label:<22} timeout {timeout_s:>4g}s  took {took:5.2f}s  "
          f"model calls {generate.call_count() - calls_before}  answer: {text[:40]!r}", flush=True)


if __name__ == "__main__":
    real_client = generate._get_client()
    generate.generate("warm up the connection", cache=False)   # not counted
    one_request("with the timeout", config.MODEL_TIMEOUT_S)
    one_request("without the timeout", 30)
