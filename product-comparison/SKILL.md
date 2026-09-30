---
name: product-comparison
description: Compare products, models or brands with in-depth web research based on independent lab tests, scientific studies and verified non-sponsored reviews, then build an interactive comparison sheet (short summary, filterable comparison table, adjustable-weight scoring, best verified prices with direct links, reasoned recommendation). Automatically adapts country, language and currency to the user's context. Use whenever the user wants to compare or choose between products, models, brands or a whole category ("compare", "X vs Y", "which is better", "what should I buy", "best X for...", "confronta", "quale conviene", "compara", "vergleiche", "comparer"), even if they do not ask for a sheet or give no links.
---

# Product comparison

Help the user make a purchase decision with verifiable evidence, not spec lists. The output is an interactive sheet that reads in two minutes and stands on its own: every important claim points to a source, and the recommendation also says when it is NOT the right choice.

Why it matters: online reviews are full of affiliate and sponsored content. The value here is filtering the noise, being explicit about how solid the evidence is, and never inventing data, prices or links.

## Writing rules

- Write in the user's language (see Locale below). Keep sentences short and free of sales language.
- If the user has stated style preferences (for example no em dashes), apply them to the sheet text too.

## Locale: country, language, currency (automatic)

Decide the market once, before intake, and carry it through the whole job. Infer in this order and stop at the first reliable signal:

1. What the user says explicitly ("in Germany", "in dollars", "ship to Canada").
2. Language they write in and any regional hints (units, spelling, store names, links they paste, phone or address formats).
3. Anything already known about the user in your context: stored location, country, timezone, currency, language.
4. If still unclear, ask ONE closed question during intake ("Which country should I check prices and availability for?").

From the market derive: `locale` (BCP 47, e.g. `it-IT`, `en-GB`, `de-DE`, `pt-BR`), `currency` (ISO 4217), retailers, consumer-test organisations, warranty and tax conventions. Use `references/markets.md`. For countries not listed there, follow the "Unlisted markets" procedure in that file.

Do not announce how you inferred it. Just state the assumption in the one-line recap after intake ("Market: Italy, prices in EUR") so the user can correct it. If the user's language and the market differ (Italian speaker buying in the UK), the sheet language follows the user's language and prices follow the market. Set `meta.locale` to the language plus market region when the template supports the language (en, it, es, fr, de), otherwise the sheet falls back to English UI text with correctly formatted numbers and currency.

## Workflow

### 1. Understand what to compare

Read `references/modes.md`. Four cases: specific products (names or links), brands, a generic category, one product plus "find alternatives". If the user gives a link, open it with WebFetch to identify the exact model and variant before anything else.

### 2. Intake (before any research)

Do not search before knowing the needs: the same category has different winners for different users.

- Ask 3-5 targeted questions, not a questionnaire. Skip anything the conversation or context already answers; never ask twice.
- If AskUserQuestion is available, use closed options with an obvious recommended one; otherwise list the questions in chat.
- Fixed questions: main use and frequency, budget (ceiling and whether flexible), top 3 priorities in order, constraints (size, compatibility, brands to avoid or prefer, delivery time).
- Add 1-2 category-specific questions from `references/intake.md`.
- Close with a one-line recap ("Looking for X under 400 EUR in Italy, priorities: A, B, C") and start without asking for confirmation unless something contradicts.

### 3. In-depth research

Read `references/research.md` before starting. Key points:

- Source hierarchy: independent lab tests and peer-reviewed studies, then verified reviews with methodology, then aggregated user feedback, last manufacturer claims (specs only).
- Every decisive data point needs at least two independent sources. Report disagreements, do not hide them.
- Discard "best X" listicles without their own testing, sponsored content, and reviews of free review units.
- Research each product separately: measured performance, recurring long-term problems, service and warranty in the user's market.
- For broad comparisons (more than 4 products), if sub-agents are available and the user has allowed them, parallelise per product. Otherwise work inline.

### 4. Prices and purchase links

- Find the best price by actually opening store pages with WebFetch. Price comparison sites only help discover sellers; confirm the price on the store page.
- Record per offer: store, price, verification date, shipping, sold by whom. Exclude grey market and unreliable third-party sellers, or flag them.
- Use direct product-page links stripped of tracking parameters, with no affiliate tags. Never invent a URL or price: if unverifiable, set `verified: false` and say where to check.
- Prices are the total delivered in the user's market, in the local currency, following the tax convention in `references/markets.md`.

### 5. Scoring and recommendation

- Turn the user's priorities into 4-7 criteria with weights adding to 100.
- Score 0-10 per criterion, anchored to measured data. A score without a source is an estimate and lowers data confidence.
- The recommendation weighs the weighted score, price, data confidence and known risks. If the top scorer is not your pick, explain why.
- Always include: concrete reasons (numbers and sources), "not for you if...", and 1-3 alternatives for different profiles (cheaper, top-end, special case).
- List the limits honestly: what could not be verified, old data, small samples.

### 6. Build the sheet

1. Fill a JSON file following `references/data-schema.md` (full example: `assets/example-data.json`). Text fields go in the user's language.
2. Run `python scripts/build_sheet.py data.json comparison-sheet.html`. It validates ids, score ranges, https URLs, affiliate or tracking parameters and dates, then injects the data into `assets/sheet-template.html`. Fix errors, read warnings.
3. Styling: the template uses CSS variables in `:root`. If a brand or design system is available in context, replace those values; otherwise keep the defaults.
4. Publish as an Artifact with the Artifact tool (icon `compare`) without rewriting the template. If Artifact is unavailable, deliver the HTML file: it works offline.
5. Before delivering, open the page and check: no console errors, table readable on mobile, light and dark themes.

### 7. Reply in chat

Short: one line on the recommended pick and the main reason, best verified price with date, the most important limit of the research, and the link to the sheet. Do not repeat the sheet.

## Do not

- Quote prices or specs from memory: everything comes from sources opened in this session.
- Use affiliate links. The sheet states there are none.
- Force a winner when the data does not justify one: say so and say what would settle it.
- Extend intake beyond 5 questions unless the user asks.
