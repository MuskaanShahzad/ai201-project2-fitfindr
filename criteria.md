# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
`search_listings` scores by keyword overlap with the description and drops
anything scoring zero — it isn't a semantic match. A query can describe a
listing a person would call a match without sharing a single word with that
listing's title, description, or style tags (e.g. "throwback track jacket"
vs. a listing titled "90s Track Jacket" tagged `90s`, `vintage`, `athletic`,
`streetwear` — no shared token). That's a real miss mode built into a plain
keyword matcher, not something the loop can paper over, so 4 of 5 is honest
about it rather than pretending it won't happen.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
This branch is a plain `if not search_results` check on whatever
`search_listings` already returned — Python truthiness, not another round of
keyword scoring. Nothing about phrasing matters once the result list is
already empty, so there's no variability left for a miss to hide in, unlike
criterion 1, where the match step itself is the thing that can go either way.

---

## 3. The selected item stays the same item across tool calls

For 5 different matching queries, `session["selected_item"]["id"]` equals the
`id` of `session["search_results"][0]`, and that same `id` is present in the
`new_item` dict passed into both `suggest_outfit` and `create_fit_card` — in
5 of 5 tries.

**Why this target:**
`selected_item` is a plain assignment — `session["search_results"][0]` copied
into `session["selected_item"]` — not a model call and not anything that
depends on phrasing or luck. If the id ever drifts between what search found
and what the later tools received, that's not noise, it's a bug in the loop
itself, so 5 of 5 is the only target that makes sense here.

---

## 4. The fit card stays inside its format rules

For 5 different items, a fit card counts as a pass only if it is 2-4
sentences, mentions the item's price and its platform at least once each, and
is not word-for-word identical to any of the other cards — in 4 of 5 tries.

**Why this target:**
`create_fit_card` calls the model, so it can skip part of an instruction the
same way a plain keyword matcher can miss a phrasing in criterion 1 — a flat
5 of 5 would be pretending the model never drifts from format. I'm not
worried the cards will actually come out identical (that would mean
`CACHE_ENABLED` or `TEMPERATURE` is misconfigured, not normal variance), but
I'm folding that check in here anyway rather than giving it its own number,
since it's still just one more way a single card can fail.

---

## 5. search_listings never returns a listing over the price ceiling

For 5 queries that each specify a `max_price`, every listing in
`search_results` has `price <= max_price` — in 5 of 5 tries.

**Why this target:**
`max_price` is an inclusive numeric filter applied before anything else in
`search_listings` — it's a `<=` comparison on a float, not a keyword score or
a model guess, so there's no legitimate reason a listing over the ceiling
should ever come back. Same reasoning as criterion 3: this is a deterministic
code path, not a model call, so anything less than 5 of 5 would mean the
filter itself is broken, not that the result naturally varies run to run.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->


---

# Capstone criteria

These are for the extension I built in the capstone: a server (`python serve.py`) that logs every request to `logs/runs.jsonl`. I wrote them before running any capstone trial. Every trial goes through the server over HTTP, with the cache off (`AI201_CACHE=0`), so the numbers come from real model calls. Each criterion gets five trials.

The five **matching queries** used in the trials below are always these, in this order: `vintage graphic tee under $30`, `90s track jacket in size M`, `denim jacket under $50`, `platform sneakers size 8`, `silk slip dress in midi length under $40`. The **impossible query** is always `designer ballgown size XXS under $5`.

Rules that apply to every trial:
- **Warm** means the server has already answered one request since it started. I send one throwaway request first and do not count it.
- **The log line** means the new line added to `logs/runs.jsonl` by that one request. I send nothing else to the server while a trial runs, so "exactly one new line" can be checked.
- Every trial counts. I do not throw out or redo a trial after seeing its result. The one exception is a setup mistake, such as `cache_hits` not being 0 because the cache was left on. In that case I fix the setup and rerun all five trials of that criterion, and I note that I did.
- A **non-empty string** has at least one character that is not a space. For `output`, an error message counts as non-empty.

Where the targets came from: criteria 1, 2 and 3 are about behavior, and I set them from how the system already worked. For criteria 4 and 5 I had already measured one run in the instrumentation work (about 3.3 seconds and 494 tokens on average over 12 runs), so I set those targets with that in view. I say so because a target set after seeing the numbers is easier to meet than one set blind, and I tried to set them tight enough that I could still miss them.

## Capstone 1. A matching query still completes (the original system)

I send `POST /ask` once with each of the five matching queries. For each, the response is HTTP 200, `error` is null, and `fit_card` is a non-empty string. At least 4 of the 5 pass.

**Why this target:**
Two of the three tools call the model, so a run can fail for a reason outside my code. In unit 4, one of my ten runs failed because the model could not be reached. Allowing one miss in five is the same tolerance as the 4 of 5 I used in units 3 and 4. Two misses in five would mean something is actually broken.

## Capstone 2. An impossible query stops before any model call (the original system)

I send `POST /ask` with the impossible query five times. Each time, the response is HTTP 200, `fit_card` is null, and `error` contains at least one of the words "price", "size" or "keyword" (so it tells the user what to change). The log line says `outcome` is `no_results` and `model_calls` is 0. All 5 of 5 pass.

**Why this target:**
This branch is a plain empty-list check and the model is never called, so nothing about it should vary between tries. `model_calls` is the proof that it stopped early: if it is ever above 0, the loop called a model tool with nothing to work on. I allow no misses because there is nothing random here for a miss to come from.

## Capstone 3. Every kind of request leaves one complete log line (the extension, and the bad path)

I send five requests, once each: the first matching query (should log `ok`), the second matching query (`ok`), the impossible query (`no_results`), an empty query (`rejected`), and the first matching query to a server I started with `GEMINI_API_KEY` set to a fake value (`model_unavailable`). For each one, the log gains exactly one new line. The line is valid JSON and has all ten fields (`timestamp`, `query`, `outcome`, `output`, `selected_item_id`, `latency_s`, `model_calls`, `cache_hits`, `prompt_tokens`, `output_tokens`), and `outcome` is the expected word. `timestamp`, `outcome` and `output` are non-empty strings, and the number fields are numbers. `query` is non-empty except for the rejected request, and `selected_item_id` may be null for the rejected and `no_results` ones. All 5 of 5 pass.

**Why this target:**
The log is only worth having if it covers the runs I will need to look at later, and those are the failures. Logging only successes is the easy mistake, so the five trials cover all four outcomes (`ok`, `no_results`, `rejected`, `model_unavailable`) rather than five successes. The two I care about most are a request that never reaches the agent and one that reaches the agent and then loses the model. Writing a line is plain code with no model involved, so I allow no misses.

## Capstone 4. A warm matching request finishes in 5.0 seconds or less (the extension)

I send the five matching queries to a warm server, one each. In each log line, `latency_s` (written with two decimals) is 5.0 or less. At least 4 of the 5 pass.

**Why this target:**
My 12 measured runs averaged 3.3 seconds, with two of the twelve above 5 (5.5 and 6.4). So 5.0 is not a number I am sure to meet, and with five runs there is a real chance that two of them are slow. I allow one slow run in five because model call time varies on its own, the same reason criterion 1 allows one miss. I did not pick 3.5, because the model call time varies on its own and that would fail a healthy system. I did not pick 20, because a limit that loose would let a stuck process or a rate-limit wait (30 seconds or more) look fine. `latency_s` is measured inside the server, so it leaves out the time a client spends connecting.

## Capstone 5. One matching run uses 600 tokens or fewer (the extension)

I send the five matching queries, one each. In each log line, `prompt_tokens` plus `output_tokens` is 600 or less, and `model_calls` is 2. All 5 of 5 pass.

**Why this target:**
My 12 measured runs used between 467 and 519 tokens, so 600 is about 15% above the highest one. The prompts are short and the model is asked for 2 to 4 sentences, so the count should stay near 500. A run over 600 would mean a prompt or an answer has grown well beyond what I measured, for example from a longer wardrobe or a changed prompt. I did not pick 1,000 because that would hide that kind of growth. The `model_calls` check makes sure the token count covers the full run, with both model calls made.
