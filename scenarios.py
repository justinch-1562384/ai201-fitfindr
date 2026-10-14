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
    {
        # Two near-identical listings match (lst_012 $20, lst_027 $21), so if the
        # agent swaps items between tool calls, the ids won't line up. Criterion 3.
        "name": "state carries one item through all three tools",
        "query": "oversized crewneck sweatshirt under $25",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        # One clear match: Vintage Linen Blazer, $38, thredUp. The card should
        # contain "$38", "thredUp" and the item name. Criterion 4.
        "name": "fit card names price, platform and item",
        "query": "linen blazer under $40",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # Empty wardrobe with shoes instead of outerwear (Suede Chelsea Boots,
        # lst_028), so criterion 5 isn't only tested on one category.
        "name": "empty wardrobe, different category",
        "query": "chelsea boots size 8.5",
        "wardrobe": "empty",
        "criterion": 5,
    }
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
