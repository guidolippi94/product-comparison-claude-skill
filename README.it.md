# Product Comparison — skill per Claude

[English](README.md)

Confronta prodotti, modelli o marchi con ricerca web su test di laboratorio indipendenti e recensioni verificate non sponsorizzate, poi consegna una **scheda comparativa interattiva** (HTML, funziona offline o come Artifact di Claude):

- sintesi e scelta consigliata, con "non fa per te se..." e alternative
- tabella filtrabile e ordinabile, **slider delle priorità** che aggiornano la classifica in tempo reale
- prezzi migliori verificati con link diretti (senza tag affiliati) e data di verifica
- fonti classificate per tipo e indipendenza, più l'elenco di ciò che non è stato possibile verificare

Paese, lingua e valuta si deducono dal contesto. Interfaccia scheda: EN, IT, ES, FR, DE. Un validatore integrato blocca link affiliati/di tracciamento, id incoerenti e punteggi fuori scala.

## Installazione

**Claude Code**

```bash
git clone <repo-url> && cd product-comparison-skill
cp -r product-comparison ~/.claude/skills/
```

(Solo per un progetto: copia in `<progetto>/.claude/skills/`.)

**Claude.ai / Desktop** — comprimi la cartella della skill e caricala in *Impostazioni → Capacità → Skills*:

```bash
zip -r product-comparison.zip product-comparison -x "*/__pycache__/*"
```

Richiede Python 3 (solo libreria standard) e accesso al web per la ricerca.

## Uso

Basta chiedere:

- "Confronta Sony WH-1000XM6 e Bose QuietComfort Ultra."
- "Quale robot aspirapolvere compro sotto i 400 euro? Ho due gatti."
- "Lavatrici Bosch vs Miele vs Siemens."
- "Ci sono alternative migliori a questo? https://..."

Claude fa 3–5 domande, ricerca, costruisce la scheda e ti dà un link o un file HTML.

## Struttura

```
product-comparison/   la skill (installa questa cartella)
  SKILL.md            flusso e regole
  references/         modalità, intake, metodo di ricerca, mercati, schema JSON
  assets/             template scheda + dati di esempio
  scripts/            build_sheet.py (validatore + generatore)
examples/             dati di esempio e schede generate
tests/                test unitari
```

## Personalizzazione

- **Aspetto**: variabili CSS in `assets/sheet-template.html` (`:root`).
- **Lingua UI**: aggiungi un blocco all'oggetto `T` nel template.
- **Mercato**: aggiungi una riga a `references/markets.md`.
- **Regole di ricerca**: `references/research.md`.

Sviluppo: `python -m unittest discover tests`

## Limiti

- Nessun dato inventato: prezzi, specifiche e link vengono da pagine aperte in sessione; ciò che non si verifica è segnato.
- I prezzi cambiano; ogni offerta mostra la data di verifica.
- Poche fonti indipendenti → etichetta di bassa affidabilità, non un punteggio sicuro.
- Le indicazioni su salute e sicurezza sono solo informative.

## Licenza

MIT, vedi [LICENSE](LICENSE).
