"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import re

import config
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    query_words = _words(description or "")
    if not query_words:
        return []

    scored = []
    for listing in load_listings():
        if max_price is not None and listing["price"] > max_price:
            continue
        if size and not _size_matches(size, listing["size"]):
            continue

        score = _score(query_words, listing)
        if score > 0:
            scored.append((score, listing))

    # sorted() is stable, so ties keep the order they have in listings.json
    scored = sorted(scored, key=lambda pair: pair[0], reverse=True)
    return [listing for _, listing in scored[: config.SEARCH_RESULT_LIMIT]]


# Words that say nothing about the item. Without this, "a top for the summer"
# scores every listing whose description contains "the".
_STOPWORDS = {
    "a", "an", "and", "the", "for", "with", "in", "of", "to", "on", "or",
    "i", "im", "me", "my", "want", "need", "looking", "something", "some",
    "under", "size", "that", "is", "it",
}


def _words(text: str) -> set[str]:
    """Lowercase words with a trailing plural 's' dropped, so 'tees' meets 'tee'."""
    words = set()
    for word in re.findall(r"[a-z0-9]+", text.lower()):
        if word in _STOPWORDS:
            continue
        if len(word) > 3 and word.endswith("s"):
            word = word[:-1]
        words.add(word)
    return words


def _score(query_words: set[str], listing: dict) -> int:
    """
    Count query words found in the listing. A hit in the title, category or
    style tags counts 2, a hit only in the description, colors or brand
    counts 1. A word the seller put in the title says more about the item than
    one mentioned in passing in the description.
    """
    strong = _words(" ".join([
        listing["title"], listing["category"], " ".join(listing["style_tags"]),
    ]))
    weak = _words(" ".join([
        listing["description"], " ".join(listing["colors"]), listing["brand"] or "",
    ]))
    return sum(2 if w in strong else 1 if w in weak else 0 for w in query_words)


def _size_matches(wanted: str, listing_size: str) -> bool:
    """
    Whole-token size matching, case-insensitive.

    A listing size is split on '/' into options, with any parenthetical note
    dropped: "S/M" offers "s" and "m", "XL (oversized)" offers "xl", and
    "One Size / Oversized" offers "one size" and "oversized". The wanted size
    matches if it equals one of those options, or one space-separated word of
    an option, so "W30" matches "W30 L30".

    Never a substring test: "S" must not match "US 9", and "L" must not
    match "XL" or "L30".
    """
    wanted = " ".join(wanted.lower().split())
    for option in re.sub(r"\(.*?\)", "", listing_size.lower()).split("/"):
        option = " ".join(option.split())
        if wanted == option or wanted in option.split():
            return True
    return False


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    owned = (wardrobe or {}).get("items") or []
    item = _describe_listing(new_item)

    if not owned:
        prompt = (
            f"Someone is thinking about buying this thrifted item:\n{item}\n\n"
            "They haven't told you what's in their wardrobe. Suggest one or "
            "two outfits built around this item using common basics most "
            "people own (say what kind of piece, colour and fit), and one "
            "tip on how to style it."
        )
    else:
        pieces = "\n".join(f"- {_describe_wardrobe_item(p)}" for p in owned)
        prompt = (
            f"Someone is thinking about buying this thrifted item:\n{item}\n\n"
            f"This is what they already own:\n{pieces}\n\n"
            "Suggest one or two outfits that pair the new item with pieces "
            "from their wardrobe. Name each wardrobe piece exactly as it is "
            "written above, and only use pieces from that list."
        )

    return generate(prompt, system=_STYLIST_SYSTEM)


_STYLIST_SYSTEM = (
    "You are a stylist who works with thrifted clothes. Be specific and "
    "brief: each outfit is one or two sentences. Plain text, no headings."
)


def _describe_listing(listing: dict) -> str:
    """The listing fields that matter for styling, one line each."""
    lines = [
        f"Title: {listing['title']}",
        f"Category: {listing['category']}",
        f"Colors: {', '.join(listing['colors'])}",
        f"Style: {', '.join(listing['style_tags'])}",
        f"Size: {listing['size']}",
        f"Description: {listing['description']}",
    ]
    if listing.get("brand"):
        lines.insert(1, f"Brand: {listing['brand']}")
    return "\n".join(lines)


def _describe_wardrobe_item(piece: dict) -> str:
    """One wardrobe piece on one line, e.g. 'Wide-leg khaki trousers (bottoms; khaki, tan)'."""
    details = [piece.get("category", ""), ", ".join(piece.get("colors") or [])]
    line = f"{piece['name']} ({'; '.join(d for d in details if d)})"
    if piece.get("notes"):
        line += f" — {piece['notes']}"
    return line


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    # TODO: replace this with your implementation
    return ""
