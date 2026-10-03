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

<!-- Three or four sentences: what a user asks for, and what they get back. -->



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

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

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->

**What moves through the session:** <!-- which fields, in what order -->

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'

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

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
