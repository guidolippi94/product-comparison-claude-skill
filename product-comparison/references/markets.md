# Markets: retailers, test organisations, conventions

Use this file after deciding the market (see "Locale" in SKILL.md). The lists are starting points, not exhaustive: always verify that a retailer or organisation exists and is relevant for the category today. Legal rules change, so treat the warranty notes as orientation and confirm on an official source when it matters.

| Market | locale | currency | Prices shown | Typical retailers | Test organisations and useful sources | Legal warranty (orientation) |
|---|---|---|---|---|---|---|
| Italy | it-IT | EUR | VAT included | Amazon.it, MediaWorld, Unieuro, Euronics, brand stores | Altroconsumo, Il Salvagente (food), EPREL; comparison: Idealo.it, Trovaprezzi.it | 24 months (Codice del Consumo) |
| United States | en-US | USD | Before sales tax | Amazon.com, Best Buy, Walmart, Target, B&H, Home Depot | Consumer Reports, RTINGS, Wirecutter (mixed independence), CPSC recalls | No general statutory warranty; manufacturer warranties, state lemon laws |
| United Kingdom | en-GB | GBP | VAT included | Amazon.co.uk, Currys, Argos, John Lewis, AO | Which?, RTINGS; comparison: PriceSpy, Google Shopping | Consumer Rights Act 2015 (remedies, 6 months reversed burden) |
| Germany | de-DE | EUR | VAT included | Amazon.de, MediaMarkt, Saturn, Otto, Cyberport | Stiftung Warentest, ADAC (auto), EPREL; comparison: Idealo.de, Geizhals | 2 years Gewährleistung |
| France | fr-FR | EUR | VAT included | Amazon.fr, Fnac, Darty, Boulanger, Leroy Merlin | UFC-Que Choisir, 60 Millions de consommateurs, EPREL; comparison: Idealo.fr | 2 years garantie légale de conformité |
| Spain | es-ES | EUR | VAT included | Amazon.es, PcComponentes, El Corte Inglés, MediaMarkt, Worten | OCU, EPREL; comparison: Idealo.es, Kelkoo | 3 years garantía legal (new goods) |
| Canada | en-CA | CAD | Before sales tax | Amazon.ca, Best Buy Canada, Canadian Tire, Costco | Consumer Reports, RTINGS, Health Canada recalls | Provincial rules; manufacturer warranties |
| Australia | en-AU | AUD | GST included | Amazon.com.au, JB Hi-Fi, Harvey Norman, Bunnings, Kogan | CHOICE, RTINGS, ACCC product safety | Australian Consumer Law: consumer guarantees |
| Brazil | pt-BR | BRL | Tax included | Amazon.com.br, Mercado Livre, Magazine Luiza, Americanas | Proteste, Inmetro; comparison: Zoom, Buscapé | 90 days legal (durable goods) plus manufacturer |

Cross-market sources usable everywhere when relevant: RTINGS (electronics), DXOMARK (cameras, phones), Notebookcheck (laptops), TechPowerUp (PC hardware), PubMed and Cochrane (health), EFSA and national health regulators (food and supplements).

## Unlisted markets

1. Determine `locale` and `currency` from the country (BCP 47 language-region, ISO 4217 currency).
2. Search for the country's consumer-protection organisation and its product tests (queries like "consumer organisation product tests <country>").
3. Search for the country's main electronics and general retailers and its price-comparison sites; open store pages to verify prices.
4. Search for the statutory consumer warranty and the tax convention (is VAT or GST included in shelf prices?).
5. State in `limits` that the market list was assembled during research and may be incomplete.

## Cross-border purchases

Include a foreign store only when the saving is substantial and after adding shipping, import duties or VAT, and considering warranty validity and returns. Flag it in the offer `note` (for example "ships from Germany, warranty valid in the EU").

## Currency and formatting

- The sheet formats numbers, dates and currency from `meta.locale` and `meta.currency`; write raw numbers in the JSON (`379.0`, not "379,00 €").
- When the user's language and market differ, the language sets text, the market sets prices.
- If a price is only available in another currency, do not convert silently: convert only with a stated rate and date in the note, and mark it unverified.
