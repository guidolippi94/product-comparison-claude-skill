# Data schema

The JSON file feeds `assets/sheet-template.html` through `scripts/build_sheet.py`. Full example: `assets/example-data.json`. All human-readable text goes in the user's language; keys stay in English.

## Structure

```json
{
  "meta": {
    "title": "Robot vacuums under $400",
    "short_title": "Robot vacuums",
    "category": "Home",
    "date": "2026-09-30",
    "currency": "USD",
    "locale": "en-US",
    "market": "United States",
    "method": "Optional text about how the research was done",
    "example": false
  },
  "needs": {
    "usage": "80 m2 home with two cats",
    "budget": "Up to $400",
    "priorities": ["Suction on pet hair", "Low noise", "Durability"],
    "constraints": ["No mandatory cloud"]
  },
  "summary": "2-4 sentences: what emerges from the comparison and the pick, no lists.",
  "criteria": [
    { "id": "suction", "name": "Pet hair suction", "weight": 35, "description": "Measured pickup on hair" }
  ],
  "products": [
    {
      "id": "alpha",
      "name": "Brand Model",
      "brand": "Brand",
      "official_url": "https://...",
      "scores": { "suction": 8.5 },
      "offers": [
        { "store": "Store", "price": 349.0, "url": "https://...", "date": "2026-09-30",
          "shipping": "Free, 2 days", "sold_by": "Store", "verified": true, "note": "" }
      ],
      "pros": ["..."],
      "cons": ["..."],
      "data_confidence": "high",
      "sources": ["s1", "s2"]
    }
  ],
  "feature_groups": [
    {
      "name": "Performance",
      "rows": [
        { "label": "Suction power", "unit": "Pa", "best": "high",
          "values": { "alpha": 5000, "beta": { "t": "4,000 (claimed)", "n": 4000 } },
          "note": "Measured by RTINGS: ...", "source": ["s1"] }
      ]
    }
  ],
  "pick": {
    "product_id": "alpha",
    "reasons": ["Concrete reason with a number and a source"],
    "not_for_you_if": "Condition under which another option is better",
    "alternatives": [ { "profile": "If you want to spend less", "product_id": "beta", "why": "..." } ]
  },
  "sources": [
    { "id": "s1", "title": "Article title", "publisher": "RTINGS", "url": "https://...",
      "type": "lab_test", "independence": "high", "date": "2026-05-12" }
  ],
  "limits": ["What could not be verified"]
}
```

## Fields and rules

**meta**
- `locale`: BCP 47 tag, language plus region (`it-IT`, `en-GB`, `pt-BR`). The sheet UI is translated for en, it, es, fr, de; other languages fall back to English UI text, with numbers, dates and currency still formatted for the locale.
- `currency`: ISO 4217 code. Prices in the JSON are plain numbers.
- `short_title`: page name, 2-4 words. `example: true` shows an "example data" banner; never use it for real sheets.

**criteria**: 4-7 items, integer `weight`, sum 100 (the script warns and the sheet normalises otherwise). The user can adjust weights in the sheet.

**products**
- `scores`: one value 0-10 for every criterion. Decimals allowed.
- `offers`: any order; the sheet highlights the lowest price among offers whose `verified` is not false. `price` may be `null` if unverifiable.
- `data_confidence`: `high`, `medium`, `low` (see `research.md`).
- `sources`: ids of the sources used for that product.

**feature_groups.rows**
- `best`: `high` (higher is better), `low` (lower is better), `none` (no highlighting).
- `values`: for each product id one of: number, text, `true`/`false` (shown as yes/no), `null` (n/a), or `{ "t": "displayed text", "n": number for comparison }`.
- Manufacturer-claimed values: say "(claimed)" in the text or the note.
- `source`: id or list of ids (they appear as clickable superscripts).

**pick**: `product_id` must exist. 1 to 3 `alternatives`, each for a different kind of user.

**sources**
- `type`: `lab_test`, `study`, `authority`, `verified_review`, `user_feedback`, `manufacturer`, `other`.
- `independence`: `high` (no commercial relationship), `mixed` (tests first-hand but uses affiliate links), `low` (depends on the manufacturer).
- `date`: YYYY-MM-DD.

## Generated automatically by the template

- Rows "Best verified price" and "Overall score" (updates with the weights), and "Data confidence".
- Group "Scores by criterion" derived from `scores`.
- Live ranking, best-per-row highlighting, differences-only filter, sort by score, show/hide products, light/dark theme, print.
