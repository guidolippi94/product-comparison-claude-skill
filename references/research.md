# Research: sources, reliability, prices

## Source hierarchy

Classify every source used and record it in the JSON with `type` and `independence`.

1. **Independent lab tests** (`lab_test`): repeatable measurements with public methodology, products bought by the tester. Examples: national consumer organisations (see `markets.md`), RTINGS, DXOMARK, Notebookcheck, TechPowerUp, ADAC, Euro NCAP, Which?, Consumer Reports, Stiftung Warentest.
2. **Studies and authorities** (`study`, `authority`): PubMed, Cochrane, peer-reviewed journals, food and drug regulators, energy-label databases (EPREL in the EU), safety standards. For products touching health and safety these come first; cite study design and sample size when known.
3. **Verified reviews with methodology** (`verified_review`): first-hand testing, proof of use, non-generic pros and cons, product purchased or returned. Many outlets earn affiliate commissions. That is not a reason to discard them if they really test; mark `independence: mixed`.
4. **Aggregated user feedback** (`user_feedback`): verified-purchase reviews, rating distribution, recent and long-term reviews, threads on Reddit and technical forums about recurring failures. Look for patterns, not single cases. Trustpilot-type sites are useful for stores, not products.
5. **Manufacturer data** (`manufacturer`): only for technical specs and warranty. Always flag them as claimed.

## What to discard or downgrade

- "Best X of the year" rankings without their own testing, or with descriptions copied from spec sheets.
- Sponsored content, advertorials, "in partnership with", undisclosed free review units.
- Reviews with all five stars in the same few days, repeated text, profiles without history.
- Sites listing the same three products for every query with links to a single store.
- Data for previous models attributed to the current one. Always check year and model code.

## Cross-checking and disagreements

- Every data point that weighs on the choice: at least two independent sources. With only one, say so in the row note and lower the data confidence.
- If sources disagree, report both values in the note and explain the likely reason (test method, firmware, batch).
- Prefer sources from the last 24 months; for electronics and software, the last 12. A firmware update can change behaviour: check dates.

## What to look for per product

1. Measured performance on the parameters that matter to the user (not every spec).
2. Recurring problems: failures, design defects, recalls, class actions.
3. Costs over time: consumables, spare parts, subscriptions, energy use.
4. Service and warranty in the user's market: legal warranty, commercial warranty, availability of spares, support quality.
5. Compatibility and usage constraints from intake.
6. Lifecycle: is a replacement model about to launch? Flag it, it can change the best time to buy.

## Data confidence per product

- **high**: at least two strong independent sources, recent data, no relevant disagreement.
- **medium**: one strong source plus consistent user feedback, or strong but dated sources.
- **low**: scarce sources, manufacturer data only, new product with little evidence. Say it prominently: it is not a defect of the product, it is a limit of the evidence.

## Prices and direct links

Goal: the best real price, verified today.

1. Identify sellers using the market's retailer list in `markets.md`, the manufacturer's own store, specialist shops for the category, and price-comparison sites to discover less obvious offers.
2. Open the store page with WebFetch and read price, availability, seller and shipping. If the page is unreadable, do not deduce the price: use `verified: false`.
3. The comparable price is the total delivered in the user's market (shipping included, tax per market convention). Note shipping and delivery time.
4. On marketplaces check who sells and who ships ("sold and shipped by"). Exclude parallel imports without local warranty; flag them if they are much cheaper.
5. The link goes to the product page without tracking parameters (`utm_*`, `tag=`, `ref=`, `aff*`, `gclid`, `fbclid`). If a store shows a URL with parameters, remove them and check the page is still the right one.
6. Record the verification date (YYYY-MM-DD). The sheet always presents prices as "verified on...", because they change.
7. Temporary promotions: flag them in a note and do not make them the reference price if they expire soon.

## Declaring limits

In `limits` write what the reader needs to trust the sheet: missing sources, products with few tests, unverifiable prices, data from previous years, differences between market variants, subjective criteria. A declared limit increases credibility.
