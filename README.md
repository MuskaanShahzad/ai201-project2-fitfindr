# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

FitFindr is a command-line thrifting agent. You tell it what you're looking
for in plain language — `"vintage graphic tee under $30, size M"` — and it
searches a mock listings dataset for the best match, asks a language model to
suggest an outfit pairing the find with pieces from your wardrobe, and asks it
again to write a short caption for the find like someone would actually post.
If nothing in the listings matches, it says so and tells you what to change
instead of guessing or crashing.

---

## Tool Inventory

### `search_listings`

- **What it does:** Filters the listings data by size and/or price ceiling, scores what's left by keyword overlap with the description, and returns the best matches first.
- **Inputs:** `description` (str) — free-text keywords, e.g. `"vintage graphic tee"`. `size` (str or None) — a size token to match; `None` skips size filtering. `max_price` (float or None) — inclusive price ceiling; `None` skips price filtering.
- **Returns:** A list of listing dicts, best match first, capped at `config.SEARCH_RESULT_LIMIT`. Each dict has `id` (str), `title` (str), `description` (str), `category` (str), `style_tags` (list[str]), `size` (str), `condition` (str), `price` (float), `colors` (list[str]), `brand` (str or None), `platform` (str).
- **When it has nothing:** Returns an empty list `[]` — never `None`, never an exception.

**Size match rule:** `size` matches a listing when it equals, case-insensitively, one of the listing's size field's primary tokens — the field split on `/` and whitespace, with anything in parentheses dropped first. So `"M"` matches `"S/M"` and `"XL"` matches `"XL (fits oversized)"`, but `"M"` does **not** match `"US 9"` or `"W30"`. Plain substring matching is deliberately not used — it would make `"S"` match `"US 9"` and `"L"` match `"XL"`.

### `suggest_outfit`

- **What it does:** Calls the model to suggest one or two outfit pairings between the new item and pieces already in the wardrobe, or general styling advice when the wardrobe is empty.
- **Inputs:** `new_item` (dict) — a listing dict, as returned by `search_listings`. `wardrobe` (dict) — a wardrobe dict with an `items` key holding a list of wardrobe item dicts (`id`, `name`, `category`, `colors`, `style_tags`, `notes`).
- **Returns:** A non-empty string naming one or two outfits, specific enough to mention actual wardrobe item names when the wardrobe isn't empty.
- **When it has nothing:** If `wardrobe["items"]` is empty, returns a non-empty string of general styling advice for the item instead — never an empty string, never an exception.

### `create_fit_card`

- **What it does:** Calls the model to write a short caption someone would actually post about the find, using the outfit suggestion and the item's details.
- **Inputs:** `outfit` (str) — the string returned by `suggest_outfit`. `new_item` (dict) — the listing dict for the item.
- **Returns:** A 2-4 sentence string that mentions the item, its price, and its platform once each.
- **When it has nothing:** If `outfit` is empty or whitespace-only, returns a descriptive message string (e.g. `"Can't write a caption without an outfit suggestion."`) rather than raising or returning `""`.

---

## Planning Loop

**Branch rule:** If `search_listings` returns an empty list, put a message in `session["error"]` naming what to change (loosen the price ceiling, drop the size filter, or try different keywords) and stop — return the session without calling `suggest_outfit` or `create_fit_card`. Otherwise, take the first result from `session["search_results"]`, store it in `session["selected_item"]`, and continue to `suggest_outfit` and then `create_fit_card`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex, in `agent.py::parse_query`. One pattern pulls a price ceiling out of `"under $N"`, another pulls a size out of `"size X"`; whatever text is left over (with those matched pieces and filler words like "in"/"under" stripped out) becomes the search description.

**What moves through the session:** `query` → `parsed` (`description`, `size`, `max_price` from `parse_query`) → `search_results` (from `search_listings`) → `selected_item` (`search_results[0]`) → `outfit_suggestion` (from `suggest_outfit`, given `selected_item` and `wardrobe`) → `fit_card` (from `create_fit_card`, given `outfit_suggestion` and `selected_item`). If `search_results` comes back empty, `error` is set and the session returns right there — `selected_item`, `outfit_suggestion`, and `fit_card` stay `None`.

---

## Sample Run

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'
  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Pair the Y2K butterfly baby tee with your baggy dark wash straight-leg jeans and chunky white sneakers for an effortless casual look, layering the black cropped zip hoodie on top if it gets chilly. Alternatively, tuck the baby tee into your wide-leg khaki trousers and accessorize with the brown leather belt and black combat boots for a cool contrast of styles.

  Fit card: Channeling all the early 2000s pop star energy with this butterfly baby tee. Got it on Depop for just $18 and I'm literally never taking it off. Pair it with baggy jeans and chunky sneakers for the ultimate off-duty look. ✨🦋

0 model calls this session, 2 served from cache
```

**The impossible-query path**

```
$ python app.py ask 'designer ballgown size XXS under $5'
  No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.

0 model calls this session
```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'price': 18.0, ...},
 {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'price': 24.0, ...},
 {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'price': 15.0, ...},
 {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'price': 19.0, ...},
 {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'price': 27.0, ...},
 {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'price': 26.0, ...}]
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
Pair the vintage Levi's 501s with the white ribbed tank top, layered under the oversized grey crewneck sweatshirt and finished with chunky white sneakers. Alternatively, tuck the white ribbed tank into the jeans, cinch it with the brown leather belt, and top it off with the vintage black denim jacket and black combat boots.
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Finally found the holy grail of vintage Levi's 501s and my life is officially complete. Grabbed these for $38 over on Depop and they fit like an absolute dream. Just need to throw on my beat-up white sneakers and I'm ready for the ultimate lazy-cool weekend fit.
```

**`create_fit_card`, run 3x on the same item (checking for the identical-output bug)**

```
$ python -c "
from tools import create_fit_card
from utils.data_loader import load_listings
item = load_listings()[0]
for i in range(3):
    print(f'--- run {i+1} ---')
    print(create_fit_card('jeans and white sneakers', item))
"
--- run 1 ---
The search for the perfect vintage wash is officially over. Scored these broken-in 501s for just $38 over on depop and I'm never taking them off. Throwing these on with a crisp white tee and beat-up sneakers for the ultimate off-duty model vibe.
--- run 2 ---
Found the holy grail of denim today. These vintage 501s in the perfect medium wash are giving the ultimate 90s off-duty model vibe. Just grabbed them on Depop for $38 and honestly, I'll probably live in these with my beat-up white sneakers all fall.
--- run 3 ---
Finally found my holy grail vintage 501s and I'm literally never taking them off. Scored this medium wash perfection for just $38 on Depop. Just need to style them with my beat-up white sneakers and the effortless 90s fit is complete.
```

All three are different — not a `CACHE_ENABLED`/`TEMPERATURE` bug.

**Empty-case checks, all three tools**

```
$ python -c "
from tools import search_listings, suggest_outfit, create_fit_card
from utils.data_loader import get_empty_wardrobe, load_listings
print('empty search:', search_listings('designer ballgown', size='XXS', max_price=5))
print('empty wardrobe:', suggest_outfit(load_listings()[0], get_empty_wardrobe()))
print('empty outfit:', create_fit_card('', load_listings()[0]))
"
empty search: []
empty wardrobe: Pair these medium-wash 501s with a cropped white baby tee and chunky black loafers for an effortless, classic streetwear look. Alternatively, layer an oversized forest green or heather gray crewneck sweatshirt over a tucked-in vintage graphic tee.
empty outfit: Can't write a caption without an outfit suggestion.
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* I was drafting criteria 3, 4, and 5 for `criteria.md`
  with Claude and had it propose confidence targets for each one.
- *What came back:* It proposed a flat 5 of 5 for criterion 4 (the fit card),
  even though `create_fit_card` calls the model — the exact same reasoning it
  had just used two sections earlier to justify a *looser* 4 of 5 on
  criterion 1, which also calls the model. It had also left criterion 5 at
  10 of 10.
- *What I changed:* I caught that two criteria involving the same kind of
  thing — a model call — were being held to different standards, and asked
  directly whether 5/5 and 10/10 across the board was overconfident. We
  reworked criterion 4 so the part a model can realistically get wrong
  (sentence length, mentioning the price and platform) dropped to 4 of 5,
  while the "no two cards identical" check — which only catches a config bug
  (`CACHE_ENABLED` or `TEMPERATURE`), not normal model variation — stayed at
  5 of 5. When the two-number version read as confusing, I had it fold both
  checks into one criterion with a single target instead.

**Moment 2**

- *What I asked for:* I had Claude write the size-matching rule for
  `search_listings`, since the starter's own docstring warned that a naive
  substring check would be buggy — `"s" in "us 9"` and `"l" in "xl"` are both
  `True` in Python.
- *What came back:* Claude pulled every distinct size string out of
  `data/listings.json` first (`S`, `S/M`, `W30 L30`, `US 8.5`,
  `XL (fits oversized)`, etc.), then proposed a rule: split each listing's
  size field on `/` and whitespace, drop anything in parentheses, and match
  only on exact token equality instead of substrings.
- *What I changed:* Nothing in the rule itself — I verified it independently
  once `tools.py` was built, by calling `_size_matches` directly on the exact
  edge cases (`"M"` vs `"S/M"` → true, `"M"` vs `"US 9"` → false, `"XL"` vs
  `"XL (fits oversized)"` → true) before trusting it in the real search flow.

**Moment 3 — Unit 4, Milestone 4**

- *What I asked for:* I handed Claude all five verdicts (all MET) and asked it to push back on each one as hard as it could instead of just agreeing with a clean result.
- *What came back:* It didn't just restate the verdicts — it found two places
  where "MET" was resting on weaker evidence than it looked. Criterion 3's
  "same id across all three tool calls" claim was only checked by matching
  *titles* in the saved run; the actual trace line for `create_fit_card` gets
  cut off by `trace.py`'s 110-character limit before it ever reaches the
  `item=` part, so that half of the claim had never really been measured.
  Criterion 4's sentence count had been done by eye and come out suspiciously
  clean (3 sentences, every card) — Claude checked it with a script instead,
  which caught a bug in itself on the first try (a guard meant to protect
  against misreading "$18." as a sentence break also blocked a real break
  after "$30!", undercounting one card).
- *What I changed:* I had it close both gaps with real evidence rather than
  just argument — re-running criterion 3 with `suggest_outfit`/
  `create_fit_card` stubbed out to capture the literal `.id` passed at each
  call site, and fixing the regex before trusting criterion 4's count. The
  criterion-3 gap is also what Milestone 5's one improvement fixed directly in
  `agent.py`, so the trace itself shows the id now instead of needing a
  stand-in script.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════ -->

## Run Log — Before

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. The selected item stays the same item across tool calls | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. The fit card stays inside its format rules | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. search_listings never returns a listing over the price ceiling | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**How the five tries were produced** (`scenarios.py`, run through
`run_eval.py::main` → `run_eval.py::run_once` → `agent.py::run_agent`):

- Criteria 1 and 2 call the model (or, for criterion 2, hit the branch that
  skips the model), so the thing worth varying across 5 tries is the model's
  answer to the *same* input. Each is one scenario in `scenarios.py`
  (`"matching query completes"`, `"impossible query stops early"`), run 5
  times with caching off: `python run_eval.py --label before_A --tries 5`.
- Criteria 3, 4, and 5 are each written as "5 *different* queries/items," not
  "the same input 5 times" — criterion 3 and 5 are plain deterministic code
  paths with nothing for repetition to reveal, and criterion 4 explicitly asks
  for different items. Each got 5 separate scenario entries in
  `scenarios.py` (e.g. `"price ceiling 1"` … `"price ceiling 5"`), run once
  each: `python run_eval.py --label before_B --tries 1`. Try 1-5 in the table
  above are those 5 distinct scenarios' single tries, not repeats.
- Full raw output for both passes: `results/run_2026-10-07_2056_before_A.md`
  and `results/run_2026-10-07_2059_before_B.md`.

**Real output from one try**, pasted as text, naming the file and function
that produced it. All five below come from `agent.py::run_agent`, invoked by
`run_eval.py::run_once`.

**Criterion 1** — `matching query completes`, try 1, query `vintage graphic tee under $30`:

```
[1] search_listings (via MCP)
      in:  description='vintage graphic tee', size=None, max_price=30.0
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[2] suggest_outfit
      in:  new_item='Y2K Baby Tee — Butterfly Print', wardrobe_items=10
      out: Pair the Y2K butterfly baby tee with your baggy dark-wash straight-leg jeans and chunky white sneakers for an …
[3] create_fit_card
      in:  outfit='Pair the Y2K butterfly baby tee with your baggy dark-wash straight-leg jeans and chunky white sneakers…
      out: Found the ultimate Y2K butterfly baby tee and I’m literally obsessed. Got it listed on Depop for just $18 so y…

fit_card: "Found the ultimate Y2K butterfly baby tee and I’m literally obsessed. Got it listed on Depop for just $18 so you can live out all your early 2000s pop star dreams. Pair it with baggy jeans and chunky sneakers for the absolute easiest casual fit. ✨"
```

**Criterion 2** — `impossible query stops early`, try 1, query `designer ballgown size XXS under $5`:

```
[1] search_listings (via MCP)
      in:  description='designer ballgown', size='XXS', max_price=5.0
      out: [] (empty)
[2] branch
      →    empty search results — stopping before suggest_outfit

session["error"] = "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords."
session["fit_card"] = None  (never reached)
```

**Criterion 3** — `selected item consistency 2`, query `90s track jacket in size M`:

```
[1] search_listings (via MCP)
      in:  description='90s track jacket', size='M', max_price=None
      out: 4 items: 90s Track Jacket — Navy/White Stripe, 90s Leather Bomber — Black, 90s Silk Slip Dress — Floral, Midi Length … +1 more
[2] suggest_outfit
      in:  new_item='90s Track Jacket — Navy/White Stripe', wardrobe_items=10

session["search_results"][0]["title"] == "90s Track Jacket — Navy/White Stripe"
session["selected_item"]["title"]     == "90s Track Jacket — Navy/White Stripe"   (same object, same id)
new_item passed to suggest_outfit      == "90s Track Jacket — Navy/White Stripe"
```

**Criterion 4** — `fit card format 3`, item `90s Silk Slip Dress — Floral, Midi Length` ($30.0, depop):

```
Found my ultimate 90s grunge dream on Depop for just $30! I’m totally obsessed with throwing an oversized grey crewneck right over this floral silk midi and pairing it with chunky sneakers. Such an easy way to make a dainty slip dress feel way more *me*. ✨
```
3 sentences, mentions Depop once and $30 once, not identical to any of the other 4 cards in `results/run_2026-10-07_2059_before_B.md`.

**Criterion 5** — all 5 price-ceiling scenarios, checked directly against `tools.py::search_listings`'s output (no listing exceeds its query's `max_price`):

```
'graphic tee' max_price=30.0: prices=[18.0, 24.0, 15.0, 19.0, 27.0, 26.0]
'cargo pants' max_price=30.0: prices=[27.0]
'band tee' max_price=20.0: prices=[19.0, 18.0, 15.0]
'silk slip dress midi' max_price=40.0: prices=[30.0, 28.0]
'denim jacket' max_price=50.0: prices=[42.0, 38.0, 45.0, 24.0, 33.0, 30.0, 27.0]
```

---

## Verdicts and Diagnoses

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | A matching query completes all three tools | 4 of 5 | **MET (5/5)** | All 5 tries in `results/run_..._before_A.md` finished with a non-empty `fit_card` and a 3-step trace. 5/5 clears the 4/5 bar. |
| 2 | An impossible query stops before the second tool | 5 of 5 | **MET (5/5)** | All 5 tries stopped at the branch with `search_results == []`, before `suggest_outfit` ever ran — confirmed by the 2-step trace each time. |
| 3 | Selected item stays the same item across tool calls | 5 of 5 | **MET (5/5)** | Not just title-matching from the saved run — re-verified by stubbing `suggest_outfit`/`create_fit_card` and capturing the literal `new_item["id"]` passed to each. All 5 queries: `search_results[0].id == selected_item.id == id passed to suggest_outfit == id passed to create_fit_card`. |
| 4 | Fit card stays inside its format rules | 4 of 5 | **MET (5/5)** | Checked programmatically (sentence-splitting regex), not by eye: all 5 cards from `results/run_..._before_B.md` have 3 sentences (within 2-4), mention their price once and their platform once, and are pairwise distinct strings. |
| 5 | search_listings never returns a listing over the price ceiling | 5 of 5 | **MET (5/5)** | Called `search_listings` directly for all 5 price-ceiling queries and listed every returned price — none exceeded its query's `max_price`. |

**Diagnoses**

Nothing missed this run — but "nothing missed" isn't the same as "targets are right," so here's the honest version of that question.

- *Criterion 3*'s evidence from the saved run was thinner than it looked at first: it only showed matching *titles* between `search_results[0]`, `selected_item`, and the trace line for `suggest_outfit` — the trace line for `create_fit_card` gets cut off by `trace.py`'s 110-character line limit before it reaches the `item=` part, so that half of the claim wasn't actually measured. I re-ran all 5 queries with `suggest_outfit`/`create_fit_card` stubbed out so I could capture the literal `.id` at the call site instead. All 4 ids matched in all 5 queries (see the table above) — a real measurement now, not an inference from the code.
- *Criterion 4*: counting sentences by eye gave 3 for all 5 cards, which felt a little too clean to trust. Checking it with a regex-based sentence splitter instead caught a bug on the first pass — a guard meant to stop "$18." from being misread as a sentence break also blocked a real break after "$30!", undercounting one card as 2 sentences instead of 3. Fixed the regex, reran, and the corrected count still says 3 sentences for all 5 cards. That's exactly the kind of place a manual read could have let a real miscount slide.
- *Criterion 5*: none of the 5 test queries happen to return a listing priced exactly at its `max_price` (the closest is $45 against a $50 ceiling), so the inclusive edge of `price <= max_price` was never actually exercised — only the "nothing exceeds it" direction was. The criterion as written only claims the latter, so the verdict stands, but it's a real gap in what these 5 scenarios cover, not a gap worth glossing over.
- Criteria 1 and 2 are the most solid of the five: criterion 2 is plainly deterministic, and criterion 1 had a full, consistent trace showing every step on all 5 tries.

**On whether the 4-of-5 targets are too loose:** I'm not tightening either one, and here's why that's a judgment call rather than me dodging the question. Criterion 1's target exists because `suggest_outfit`/`create_fit_card` depend on an external model service that can fail for reasons outside the code — and this isn't hypothetical: during Milestone 2, triggering the bad-key failure on purpose also caught a *real*, unplanned `503 UNAVAILABLE` from the service on an unrelated empty-wardrobe run. That's direct evidence the failure mode criterion 1 is hedging against actually happens, even though it didn't happen in this particular 5-try window. Tightening to 5/5 off one clean run would be the same mistake as loosening a target after one bad run, just in the flattering direction. Criterion 4's target hedges against the model skipping a formatting instruction under `TEMPERATURE=0.9`; 10 fit cards across both evaluation runs (this one plus the Milestone 3 pass) have all stayed in format, which is reassuring but still a small sample against a non-deterministic generator.

If I had to name one thing worth revisiting, it's not a number — it's criterion 1's *written reason*. `criteria.md` justifies the 4-of-5 target by pointing at `search_listings`'s keyword-matching risk ("a query can describe a listing without sharing a token"), but that risk is actually part of the criterion's precondition ("given a query that *matches*"), not something the test measures. What criterion 1 actually exercises is tool-call completion under real service conditions — a different risk than the one written down. The number still looks right for that actual risk; the explanation underneath it is answering a different question. I'm not revising it, since the criterion itself is measurable and the target isn't wrong — just noting it so the reasoning in `criteria.md` and what's actually being tested don't quietly drift apart.

---

## Loop Trace

**Happy path**

```
$ python app.py ask 'vintage graphic tee under $30' --trace
[1] search_listings (via MCP)
      in:  description='vintage graphic tee', size=None, max_price=30.0
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[2] suggest_outfit
      in:  new_item='Y2K Baby Tee — Butterfly Print', wardrobe_items=10
      out: Pair the Y2K butterfly baby tee with your baggy dark wash straight-leg jeans and chunky white sneakers for an …
[3] create_fit_card
      in:  outfit='Pair the Y2K butterfly baby tee with your baggy dark wash straight-leg jeans and chunky white sneakers…
      out: Channeling all the early 2000s pop star energy with this butterfly baby tee. Got it on Depop for just $18 and …

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Pair the Y2K butterfly baby tee with your baggy dark wash straight-leg jeans and chunky white sneakers for an effortless casual look, layering the black cropped zip hoodie on top if it gets chilly. Alternatively, tuck the baby tee into your wide-leg khaki trousers and accessorize with the brown leather belt and black combat boots for a cool contrast of styles.

  Fit card: Channeling all the early 2000s pop star energy with this butterfly baby tee. Got it on Depop for just $18 and I'm literally never taking it off. Pair it with baggy jeans and chunky sneakers for the ultimate off-duty look. ✨🦋

0 model calls this session, 2 served from cache
```

**Empty search**

```
$ python app.py ask 'designer ballgown size XXS under $5' --trace
[1] search_listings (via MCP)
      in:  description='designer ballgown', size='XXS', max_price=5.0
      out: [] (empty)
[2] branch
      →    empty search results — stopping before suggest_outfit

  No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.

0 model calls this session
```

**On the MCP move:** `search_listings` is now called through `mcp_client.call_tool("search_listings", {...})` instead of being imported and called directly — `agent.py` no longer imports `search_listings` from `tools.py` at all. The return value didn't change: same list of listing dicts, same item picked first, same $18 Y2K Baby Tee for the same query before and after the move. The trace step is labeled `search_listings (via MCP)` so the seam is visible in the Loop Trace above, not just in the code.

**Failure modes, triggered on purpose**

- *Empty search* — `designer ballgown size XXS under $5` (data has no match). Agent stops and names what to change: *"No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords."* Trace shows the branch firing after `[1]`, before `suggest_outfit` ever runs.
- *Empty wardrobe* — `python app.py ask 'vintage graphic tee under $30' --empty-wardrobe`. `suggest_outfit` got `wardrobe_items=0` and returned general styling advice instead of wardrobe-specific pairings — a real, non-empty string, not a crash: *"Pair this Y2K butterfly baby tee with low-rise baggy cargo pants and chunky platform sneakers to lean into the nostalgic 2000s aesthetic...."*
- *Model unavailable* — changed the last character of `GEMINI_API_KEY` in `.env`, then ran a query I hadn't asked before (`retro bowling shirt under $25`) so the cache couldn't mask it. `suggest_outfit` raised `ModelUnavailable`, caught in `run_agent()`, which set `session["error"]` and returned before `create_fit_card` ran: *"The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com."* Key restored immediately after.

  One honest note: on the first two attempts at the empty-wardrobe run, the real model backend returned a transient `503 UNAVAILABLE` ("experiencing high demand") — not something I triggered. The same `ModelUnavailable` handler caught that too, with no crash, which is a second (unplanned) confirmation that the handler works for any reason the model can't be reached, not just a bad key.

---

## The Improvement

**What I changed:** In `agent.py::run_agent`, I reordered the `trace.step()` input strings for `suggest_outfit` and `create_fit_card`, and added each listing's actual `id` (not just its title) to both. Before: `inputs=f"outfit={...!r}, item={...title!r}"` — the long `outfit` text always came first, so `trace.py`'s 110-character line limit cut the line off before it ever reached `item=`. After: `inputs=f"item_id={...id!r}, item={...title!r}, outfit={...!r}"` — identity comes first, so it's never the part that gets truncated away, and `item_id` is the literal field criterion 3 is about.

**Which failure it was meant to fix:** Not a PASS/FAIL miss — Milestone 4's diagnosis for criterion 3 found an evidence gap, not a behavior bug: the saved trace couldn't actually show whether the right item's `id` reached `create_fit_card`, so I had to write a separate script that stubbed out the tool calls just to get real proof. This fixes that gap directly in the trace itself.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | FAIL | MET (4/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. The selected item stays the same item across tool calls | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. The fit card stays inside its format rules | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. search_listings never returns a listing over the price ceiling | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Same methodology as the before-run: criteria 1 and 2 are one scenario each, run 5 times (`--label after_A --tries 5`); criteria 3-5 are 5 different scenarios, run once each (`--label after_B --tries 1`). Raw output: `results/run_2026-10-07_2250_after_A.md` and `results/run_2026-10-07_2253_after_B.md`.

**Criterion 3, directly from the saved trace now** (`results/run_..._after_B.md`, `selected item consistency 2`):

```
[2] suggest_outfit
      in:  new_item_id='lst_004', new_item='90s Track Jacket — Navy/White Stripe', wardrobe_items=10
[3] create_fit_card
      in:  item_id='lst_004', item='90s Track Jacket — Navy/White Stripe', outfit='Pair the 90s track jacket with your wh…
```

Compare to the before-run's version of the same line: `in:  outfit='Pair the Y2K butterfly baby tee with your baggy dark-wash straight-leg jeans and chunky white sneakers…` — cut off before `item=` ever appeared. The id is now the first thing on the line in every scenario, every time.

**Did it help, and how do I know:** Yes, for what it was actually meant to fix — but it's a narrow kind of help, and the honest version of this answer has two parts.

It fixed the evidence gap exactly as intended: criterion 3's id-match is now visible directly in a saved `run_eval.py` output file, for every scenario, with nothing truncated away. Before this change, that same claim required a separate one-off script stubbing out `suggest_outfit`/`create_fit_card` to capture the real `.id` — useful once, but not something a plain re-run of `run_eval.py` would ever show. Now it's just... there, in the log, every time.

It did **not** change any PASS/FAIL outcome, and it couldn't have — the change only touches what gets printed to the trace, not what the agent does. So the two runs are a fair comparison of the same behavior, not a before/after of a bug getting fixed. The one real difference in the numbers (criterion 1 dropped from 5/5 before to 4/5 after) wasn't caused by my change either — it was a second, unplanned real failure: try 5 hit an actual `ModelUnavailable` (`Server disconnected without sending a response`), caught cleanly with no crash, same as the `503` from Milestone 2. That's not a problem with the code; if anything it's reassuring in a different way, since it's live evidence that criterion 1's 4-of-5 target reflects a real failure mode rather than a hypothetical one, and the agent handled it exactly as designed.

---

## What's Still Broken

Nothing was missed, so there's no bug to fix — just honest notes on what's left open:

- **Criterion 4's target (4 of 5) might be too easy.** Both test runs gave 10 clean fit cards total with no format problems, while criterion 1 actually failed once. I'd raise criterion 4 to **5 of 5** in `criteria.md`, but 5 tries per run isn't enough to commit to a new number yet, so I'm leaving it as is.
- **Criterion 5 was only tested below the price ceiling, never exactly at it.** I'd add one more test query where a listing's price matches the ceiling exactly.
- **Criterion 1's written reason doesn't match what's actually being tested.** `criteria.md` blames keyword search for the risk; what's really being tested is whether the model stays reachable. The number (4 of 5) is still right — just the reason under it isn't.

Criteria 2 and 3 have nothing open — neither depends on the model, and both passed cleanly every time.

📖 **How to run this project: [RUNNING.md](RUNNING.md)**


---

## Capstone

**The System**

FitFindr, the same repo and code from units 3 and 4.

**The Shape**

Shape A (deploy and instrument) on Path B (local, with logs). Until now FitFindr only ran when I typed a command in my terminal, and the only record of a run was what I copied by hand. I'm adding a server start command (`serve.py`) and a log that writes one JSON line per request: when it ran, the query, what came out, how long it took, and how many tokens it used. Success, no results and model failure all get logged. The log also gives me the cost and latency numbers.

**Out of Scope**

- No hosting. Path B only needs a start command and a committed log.
- No changes to the agent: tools, prompts, search and loop stay as they are.
- No new failure handling (retries, timeouts). A failed run gets logged, not fixed.
- No stretch items.

**Size Check**

One small logging wrapper around `run_agent`, one call to it in `serve.py`, a script that sends requests, and a new `RUNNING.md`. About an hour of building.


**Instrumentation**

Every request that reaches `serve.py` writes one line to `logs/runs.jsonl`. The code is `runlog.py` (`run_logged` wraps `run_agent`; `serve.py` calls it). Each line is a JSON object with these fields:

- `timestamp`: when the request finished (UTC)
- `query`: what the user typed
- `outcome`: `ok`, `no_results`, `model_unavailable`, `exception`, or `rejected`
- `output`: the fit card if it worked, otherwise the error message
- `selected_item_id`: the listing the agent picked (null if none)
- `latency_s`: seconds from the start of the run to the end, measured inside the server
- `model_calls`, `cache_hits`: how many model requests the run sent, and how many answers came from the cache
- `prompt_tokens`, `output_tokens`: token counts reported by the model service

`python runlog.py` prints the whole log as a short table. The full file is committed (22 lines). Failures are logged too: `no_results` (nothing matched), `model_unavailable` (the model could not be reached), `exception` (anything else that crashed the run), and `rejected` (a request with no query, which gets a 400 and never reaches the agent).

How the session was produced: the server was started with the cache off (`$env:AI201_CACHE='0'; python serve.py`). I ran `python drive.py` twice, 60 seconds apart so the rate limiter would not add waiting time. I then sent one empty query. Last, I restarted the server with a wrong API key (`GEMINI_API_KEY=not-a-real-key`) and ran `drive.py` once more.

Ten entries from the session (the first ten lines of the log). Nine are `ok`. The seventh (the ballgown query) is `no_results`: an impossible query that stopped before any model call, so it shows 0 tokens:

```json
{"timestamp": "2026-11-12T01:26:22+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Found the ultimate Y2K butterfly baby tee and I’m literally obsessed. Manifesting warm weather vibes with this one, grabbed it on Depop for just $18. Pair it with baggy denim and chunky sneakers for that effortless fitted-meets-baggy look.", "selected_item_id": "lst_002", "latency_s": 5.49, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 365, "output_tokens": 103}
{"timestamp": "2026-11-12T01:26:27+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Found this absolute holy grail 90s navy and white striped track jacket and I am officially obsessed. Scored it on Poshmark for just $45 and the sporty streetwear vibes are immaculate. Honestly can't wait to style it with baggy denim and chunky sneakers all fall long. ✨", "selected_item_id": "lst_004", "latency_s": 2.53, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 389, "output_tokens": 130}
{"timestamp": "2026-11-12T01:26:32+00:00", "query": "silk slip dress in midi length under $40", "outcome": "ok", "output": "Found the ultimate 90s dream dress and honestly, I’m never taking it off. Grabbed this floral midi on Depop for $30 and I’m obsessed with the grunge-meets-femme vibe. Layer it over a baby tee with chunky sneakers, or throw an oversized crewneck right on top for chilly days. 🥀✨", "selected_item_id": "lst_013", "latency_s": 3.13, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 380, "output_tokens": 127}
{"timestamp": "2026-11-12T01:26:41+00:00", "query": "platform sneakers size 8", "outcome": "ok", "output": "Found my new daily uniform on Poshmark for $48. Absolutely obsessed with the chunky Y2K streetwear vibe of these platforms. Can’t wait to live in these all fall.", "selected_item_id": "lst_019", "latency_s": 6.35, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 372, "output_tokens": 99}
{"timestamp": "2026-11-12T01:26:45+00:00", "query": "denim jacket under $50", "outcome": "ok", "output": "Obsessed with this light-wash cropped denim jacket for nailing that effortless double-denim look. Snagged it on Poshmark for $42 and the fit is honestly just too good. Perfect for throwing over a hoodie or a basic tank when you want that 90s streetwear vibe.", "selected_item_id": "lst_007", "latency_s": 2.34, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 374, "output_tokens": 125}
{"timestamp": "2026-11-12T01:26:50+00:00", "query": "cargo pants under $30", "outcome": "ok", "output": "Finally found the ultimate 2000s off-duty model cargos. Scored them on Poshmark for just $27 and I am so obsessed with this utility vibe. Gonna style them with a baby tee and combat boots for that effortless Y2K street style.", "selected_item_id": "lst_011", "latency_s": 2.69, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 364, "output_tokens": 103}
{"timestamp": "2026-11-12T01:26:53+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.4, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T01:28:00+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Living out my inner 2000s pop star dreams in this little butterfly tee. ✨ Only $18 over on my Depop if you want to channel major Y2K mall rat energy. I’m obsessed with how it looks paired with baggy jeans and chunky sneakers.", "selected_item_id": "lst_002", "latency_s": 3.03, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 383, "output_tokens": 124}
{"timestamp": "2026-11-12T01:28:06+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Found my new everyday throw-on jacket and I am obsessed with this sporty 90s streetwear vibe. Scored it on Poshmark for $45 and honestly haven't stopped wearing it since. Throwing it over a baby tee with some baggy jeans is about to be my whole personality.", "selected_item_id": "lst_004", "latency_s": 2.98, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 386, "output_tokens": 129}
{"timestamp": "2026-11-12T01:28:11+00:00", "query": "silk slip dress in midi length under $40", "outcome": "ok", "output": "Found my new uniform for the next three months. Got this 90s floral silk midi on Depop for just $30 and honestly, I’m never taking it off. It’s giving grungy-romance if you throw it on with chunky boots and a beat-up denim jacket, or total cozy lazy-day energy with an oversized crewneck. 🥀✨", "selected_item_id": "lst_013", "latency_s": 3.11, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 380, "output_tokens": 131}
```

Two failed runs from the same log, the empty query and one run with the wrong key:

```json
{"timestamp": "2026-11-12T01:28:28+00:00", "query": "", "outcome": "rejected", "output": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "selected_item_id": null, "latency_s": 0.0, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T01:28:46+00:00", "query": "vintage graphic tee under $30", "outcome": "model_unavailable", "output": "The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.", "selected_item_id": "lst_002", "latency_s": 5.0, "model_calls": 1, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
```

The wrong-key run is `model_unavailable` with 0 tokens: the search worked, the model call was refused, and the agent stopped with a message instead of crashing. The `exception` outcome did not come up in this session, so I have not seen it write a line.

**What It Costs**

I measured the cost of one matching run from the 12 `ok` runs in the log above. The model service reports the token counts for each call, and `runlog.py` adds up the two calls in a run (`suggest_outfit` and `create_fit_card`). The cache was off, so every number is a real model call. This is a measurement, not a number from the pricing page.

| One matching run | Average | Lowest | Highest |
|---|---|---|---|
| Prompt tokens | 376 | 364 | 389 |
| Output tokens | 118 | 99 | 131 |
| Total tokens | 494 | 467 | 519 |
| Seconds (`latency_s`) | 3.3 | 2.3 | 6.4 |
| Model calls | 2 | 2 | 2 |

So one run costs about **500 tokens and about 3 seconds**. The median time is 3.0 seconds; the one 6.4-second run is a single slow run and I did not look into why. A query that matches nothing costs 0 tokens and about 1.3 seconds, which is the time the MCP search takes on its own (it starts a separate Python process). I am on the free tier, so the money spent was $0, and I have not turned the tokens into dollars because I did not measure a price.

One note on the clean-clone test: it passed the first time, so nothing was missing from `RUNNING.md`. The only fix was in my own first draft, where a curl example would have lost the `$30` in the query. I replaced it before committing.


**Run Log Before**

This is the test of the extension before any fix. I ran it with `python run_capstone.py --label before --runs 3`. One run is the whole test once: five trials for each criterion, scored exactly as `criteria.md` words them. I repeated the whole test three times with the cache off and nothing changed in between, waiting 60 seconds between runs. The script (`run_capstone.py`) starts `serve.py`, sends every request over HTTP, and reads the log line each request wrote. The full output is in `results/capstone_before.md`, and the log lines are in `logs/runs.jsonl`.

How I read the table: each cell is how many of that run's 5 trials passed. A criterion is MET only if all three runs reach its target. Criteria 1, 4 and 5 are scored from the same five matching requests in each run (the response for criterion 1, the log line's `latency_s` for criterion 4, its tokens and `model_calls` for criterion 5). Before the real runs I did one throwaway dry run to catch bugs in the test script. I restored the log and deleted its output, so it is not in these results.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. A matching query completes | at least 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. An impossible query stops before any model call | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Every kind of request leaves one complete log line | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. A warm matching request takes 5.0 s or less | at least 4 of 5 | 5/5 | 3/5 | 4/5 | MISSED |
| 5. One matching run uses 600 tokens or fewer | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

Criterion 4 is the only miss: run 2 had 3 of 5 and run 3 had 4 of 5. The other four criteria hit their target in every run.

The output below is real, copied from `results/capstone_before.md`. Each log line was written by `runlog.py::run_logged` for a request that `run_capstone.py::one_run` sent.

*Criterion 1, run 1.* The five matching queries. Each returned HTTP 200 with a fit card (the `output` field is the fit card), 5 of 5:

```json
{"timestamp": "2026-11-12T02:14:31+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Found the ultimate Y2K baby tee with the cutest pastel butterfly print. Grabbed it on Depop for just $18 and I’m already obsessed. Throwing it on with baggy dark-wash denim and chunky sneakers for that 2000s off-duty model vibe. ✨🦋", "selected_item_id": "lst_002", "latency_s": 3.47, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 366, "output_tokens": 112}
{"timestamp": "2026-11-12T02:14:34+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Living out my 90s streetwear dreams in this navy and white striped track jacket. Snagged it on Poshmark for $45 and honestly, I'm never taking it off. Throwing it over a white ribbed tank and baggy denim is about to be my entire personality this season.", "selected_item_id": "lst_004", "latency_s": 3.32, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 382, "output_tokens": 125}
{"timestamp": "2026-11-12T02:14:37+00:00", "query": "denim jacket under $50", "outcome": "ok", "output": "Obsessed with how good this cropped light wash jacket looks thrown over literally everything. Paid $42 on Poshmark and it’s giving the ultimate effortlessly cool, 90s off-duty model vibe. Snag it before I change my mind and keep it for myself!", "selected_item_id": "lst_007", "latency_s": 2.57, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 367, "output_tokens": 114}
{"timestamp": "2026-11-12T02:14:40+00:00", "query": "platform sneakers size 8", "outcome": "ok", "output": "Scored these chunky white platforms on Poshmark for just $48 and I am officially in my Y2K model-off-duty era. Going to live in these with baggy denim and a vintage jacket all fall. Honestly, the ultimate lazy-girl street style hack.", "selected_item_id": "lst_019", "latency_s": 2.73, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 375, "output_tokens": 120}
{"timestamp": "2026-11-12T02:14:43+00:00", "query": "silk slip dress in midi length under $40", "outcome": "ok", "output": "Finally found my dream 90s floral slip dress and I am never taking it off. Got this midi beauty on Depop for just $30 and the grunge-meets-feminine styling options are endless. Obsessed with layering it over a white ribbed tank with chunky sneakers, or just throwing an oversized crewneck right over top.", "selected_item_id": "lst_013", "latency_s": 3.65, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 393, "output_tokens": 135}
```

*Criterion 2, run 1.* The impossible query, first two of five. `outcome` is `no_results`, `model_calls` is 0, and `output` is the message naming what to change:

```json
{"timestamp": "2026-11-12T02:14:45+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.31, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:14:46+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.36, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
```

*Criterion 3, run 1.* The five requests in order: `ok`, `ok`, `no_results`, `rejected` (the empty query), and `model_unavailable` (the wrong-key server). Each wrote exactly one line with all ten fields:

```json
{"timestamp": "2026-11-12T02:15:27+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Obsessed with this little butterfly tee—giving major 2000s pop star off-duty vibes. Got it on Depop for just $18 and I’m already living in it. Paired it with my go-to baggy jeans and a beat-up denim jacket for the ultimate nostalgic look. 🦋✨", "selected_item_id": "lst_002", "latency_s": 5.27, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 367, "output_tokens": 118}
{"timestamp": "2026-11-12T02:15:29+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Found the ultimate 90s streetwear piece and I'm obsessed. Snagged this navy and white stripe track jacket for just $45 over on Poshmark. Throw it on with a ribbed tank, baggy denim, and chunky sneakers for that effortless model-off-duty vibe.", "selected_item_id": "lst_004", "latency_s": 2.38, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 388, "output_tokens": 129}
{"timestamp": "2026-11-12T02:15:30+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.42, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:15:30+00:00", "query": "", "outcome": "rejected", "output": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "selected_item_id": null, "latency_s": 0.0, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:15:37+00:00", "query": "vintage graphic tee under $30", "outcome": "model_unavailable", "output": "The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.", "selected_item_id": "lst_002", "latency_s": 5.36, "model_calls": 1, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
```

*Criterion 4, run 2 (the run that missed).* `latency_s` for the five matching queries was 2.67, 2.58, 6.89, 6.96 and 3.29, so 3 of 5 were 5.0 or less:

```json
{"timestamp": "2026-11-12T02:16:45+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Found the absolute cutest butterfly tee on Depop for just $18! Obsessed with this pastel Y2K vibe. Gonna pair it with my go-to baggy jeans and a vintage denim jacket for the ultimate effortless look.", "selected_item_id": "lst_002", "latency_s": 2.67, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 371, "output_tokens": 100}
{"timestamp": "2026-11-12T02:16:48+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Found the ultimate 90s streetwear piece and I’m obsessed. Snagged this navy and white striped track jacket for $45 over on Poshmark. Throwing it on over a white ribbed tank and baggy denim is about to be my entire personality this season.", "selected_item_id": "lst_004", "latency_s": 2.58, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 380, "output_tokens": 118}
{"timestamp": "2026-11-12T02:16:55+00:00", "query": "denim jacket under $50", "outcome": "ok", "output": "Obsessed with this light wash cropped denim jacket I just scored on Poshmark for $42. It’s giving major off-duty model vibes, whether I throw it over a ribbed tank and khakis or layer it heavy-duty style with a baggy crewneck and combat boots. Such a good closet staple!", "selected_item_id": "lst_007", "latency_s": 6.89, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 372, "output_tokens": 126}
{"timestamp": "2026-11-12T02:17:02+00:00", "query": "platform sneakers size 8", "outcome": "ok", "output": "Obsessed is an understatement. Snagged these chunky platform sneakers on Poshmark for $48 and they instantly complete my whole Y2K streetwear vibe. Can't wait to style them with baggy denim and a vintage jacket all fall.", "selected_item_id": "lst_019", "latency_s": 6.96, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 373, "output_tokens": 111}
{"timestamp": "2026-11-12T02:17:05+00:00", "query": "silk slip dress in midi length under $40", "outcome": "ok", "output": "Obsessed is an understatement. Found this 90s floral midi on Depop for just $30 and I’m ready to live out all my grunge-romance dreams. Gonna layer it with combat boots and an oversized crewneck for that perfect messy-chic vibe. ✨🖤", "selected_item_id": "lst_013", "latency_s": 3.29, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 385, "output_tokens": 117}
```

*Criterion 5, run 1.* Uses the five lines pasted under criterion 1. `prompt_tokens` plus `output_tokens` was 478, 507, 481, 495 and 528, all 600 or less, and `model_calls` was 2 every time.

What the numbers show so far (the diagnosis comes later): the slow runs were not tied to one query, because `denim jacket under $50` took 2.57 s in run 1 and 6.89 s in run 2. Their token counts were normal. The two servers that handle the timed requests (A and C in `run_capstone.py`) hit no rate-limit pause in any run. Run 3 also had one run of 19.46 s (`silk slip dress in midi length under $40`). The first request each server answered (the warm-up) took 5.0 to 6.3 s every time, against about 3 s for the warm ones.
