"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # A query the data can match. Criterion 1.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # A query nothing can match. Criterion 2 — the branch.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # A user with nothing saved. One of unit 4's three failure modes.
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
    # Criterion 3: selected_item id must match search_results[0] id, 5
    # different matching queries. This is a plain assignment, not a model
    # call, so it needs variety in the query/data, not repeated tries of one
    # input — run these with `--tries 1`.
    {"name": "selected item consistency 1", "query": "vintage graphic tee under $30", "wardrobe": "example", "criterion": 3},
    {"name": "selected item consistency 2", "query": "90s track jacket in size M", "wardrobe": "example", "criterion": 3},
    {"name": "selected item consistency 3", "query": "silk slip dress in midi length under $40", "wardrobe": "example", "criterion": 3},
    {"name": "selected item consistency 4", "query": "platform sneakers size 8", "wardrobe": "example", "criterion": 3},
    {"name": "selected item consistency 5", "query": "denim jacket under $50", "wardrobe": "example", "criterion": 3},

    # Criterion 4: fit card format rules, 5 different items. Run with
    # `--tries 1` — one card per item, not the same item five times.
    {"name": "fit card format 1", "query": "vintage graphic tee under $30", "wardrobe": "example", "criterion": 4},
    {"name": "fit card format 2", "query": "90s track jacket in size M", "wardrobe": "example", "criterion": 4},
    {"name": "fit card format 3", "query": "silk slip dress in midi length under $40", "wardrobe": "example", "criterion": 4},
    {"name": "fit card format 4", "query": "platform sneakers size 8", "wardrobe": "example", "criterion": 4},
    {"name": "fit card format 5", "query": "denim jacket under $50", "wardrobe": "example", "criterion": 4},

    # Criterion 5: search_listings never returns a listing over max_price, 5
    # queries that each specify one. Deterministic filter — run with
    # `--tries 1`.
    {"name": "price ceiling 1", "query": "graphic tee under $30", "wardrobe": "example", "criterion": 5},
    {"name": "price ceiling 2", "query": "cargo pants under $30", "wardrobe": "example", "criterion": 5},
    {"name": "price ceiling 3", "query": "band tee under $20", "wardrobe": "example", "criterion": 5},
    {"name": "price ceiling 4", "query": "silk slip dress midi under $40", "wardrobe": "example", "criterion": 5},
    {"name": "price ceiling 5", "query": "denim jacket under $50", "wardrobe": "example", "criterion": 5},
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
