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
