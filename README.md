# Product Comparison — Claude skill

[Italiano](README.it.md)

Compares products, models or brands using web research on independent lab tests and verified non-sponsored reviews, then delivers an **interactive comparison sheet** (HTML, works offline or as a Claude Artifact):

- summary and recommended pick, with "not for you if..." and alternatives
- filterable table, sortable by score, **priority sliders** that re-rank live
- best verified prices with direct links (no affiliate tags) and verification date
- sources labelled by type and independence, plus a list of what could not be verified

Country, language and currency are inferred from your context. Sheet UI: EN, IT, ES, FR, DE. A built-in validator rejects affiliate/tracking links, broken ids and out-of-range scores.

## Install

**Claude Code**

```bash
git clone <repo-url> && cd product-comparison-skill
cp -r product-comparison ~/.claude/skills/
```

(Project-only: copy into `<project>/.claude/skills/` instead.)

**Claude.ai / Desktop** — zip the skill folder and upload it under *Settings → Capabilities → Skills*:

```bash
zip -r product-comparison.zip product-comparison -x "*/__pycache__/*"
```

Requires Python 3 (stdlib only) and web access for research.

## Use

Just ask:

- "Compare Sony WH-1000XM6 and Bose QuietComfort Ultra."
- "Best robot vacuum under 400 euros? I have two cats."
- "Bosch vs Miele vs Siemens washing machines."
- "Is there anything better than this? https://..."

Claude asks 3–5 intake questions, researches, builds the sheet and hands you a link or an HTML file.

## Layout

```
product-comparison/   the skill (install this folder)
  SKILL.md            workflow and rules
  references/         modes, intake, research method, markets, JSON schema
  assets/             sheet template + example data
  scripts/            build_sheet.py (validator + builder)
examples/             sample inputs and generated sheets
tests/                unit tests
```

## Customise

- **Look**: CSS variables in `assets/sheet-template.html` (`:root`).
- **UI language**: add a block to the `T` object in the template.
- **Market**: add a row to `references/markets.md`.
- **Research rules**: `references/research.md`.

Develop: `python -m unittest discover tests`

## Limits

- No invented data: prices, specs and links come from pages opened during the session; unverifiable items are marked.
- Prices change; each offer shows its check date.
- Few independent sources → low-confidence label, not a confident score.
- Health/safety advice is informational only.

## License

MIT, see [LICENSE](LICENSE).
