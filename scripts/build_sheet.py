#!/usr/bin/env python3
"""Validate product-comparison data and build the interactive HTML sheet.

Usage:
    python build_sheet.py data.json [comparison-sheet.html]

Exit code 0 when there are no errors (warnings do not block), 1 otherwise.
"""
import html
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import parse_qs, urlparse

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "sheet-template.html"
PLACEHOLDER = "/*__DATA__*/null"

TRACKING_PARAMS = {
    "tag", "ref", "ref_", "aff", "affid", "aff_id", "affiliate", "partner", "gclid", "fbclid",
    "awc", "irclickid", "clickid", "campaign", "cmpid", "linkcode", "th_hook", "smid", "cjevent",
}
AFFILIATE_HOSTS = ("amzn.to", "awin1.com", "tradedoubler.com", "shareasale.com", "anrdoezrs.net", "go.skimresources.com")
SOURCE_TYPES = {"lab_test", "study", "authority", "verified_review", "user_feedback", "manufacturer", "other"}
INDEPENDENCE = {"high", "mixed", "low"}
CONFIDENCE = {"high", "medium", "low"}
BEST = {"high", "low", "none"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LOCALE_RE = re.compile(r"^[a-z]{2,3}(-[A-Za-z0-9]{2,8})*$")
CURRENCY_RE = re.compile(r"^[A-Z]{3}$")

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def check_url(url, where, required=True):
    if not url:
        if required:
            err(f"{where}: missing URL")
        return
    p = urlparse(url)
    if p.scheme != "https":
        err(f"{where}: URL must start with https:// ({url})")
        return
    if any(p.netloc.endswith(h) for h in AFFILIATE_HOSTS):
        err(f"{where}: affiliate or shortened link, use the direct product URL ({url})")
    bad = sorted(k for k in (x.lower() for x in parse_qs(p.query)) if k in TRACKING_PARAMS or k.startswith("utm_"))
    if bad:
        err(f"{where}: remove tracking or affiliate parameters: {', '.join(bad)}")
    if p.netloc.endswith("example.com"):
        warn(f"{where}: placeholder URL (example.com)")


def check_date(value, where, required=False):
    if not value:
        if required:
            err(f"{where}: missing date")
        return
    if not DATE_RE.match(str(value)):
        err(f"{where}: invalid date '{value}' (use YYYY-MM-DD)")


def validate(d):
    for key in ("meta", "needs", "summary", "criteria", "products", "feature_groups", "pick", "sources"):
        if key not in d:
            err(f"Missing section: {key}")
    if errors:
        return

    meta = d["meta"]
    for k in ("title", "short_title", "date", "locale", "currency"):
        if not meta.get(k):
            err(f"meta.{k} is missing")
    check_date(meta.get("date"), "meta.date", required=True)
    if meta.get("locale") and not LOCALE_RE.match(meta["locale"]):
        err(f"meta.locale is not a valid BCP 47 tag: {meta['locale']}")
    if meta.get("currency") and not CURRENCY_RE.match(meta["currency"]):
        err(f"meta.currency must be a 3-letter ISO 4217 code: {meta['currency']}")
    if len(meta.get("short_title", "").split()) > 5:
        warn("meta.short_title should be 2-4 words")

    cids = [c.get("id") for c in d["criteria"]]
    if len(set(cids)) != len(cids):
        err("Duplicate criteria ids")
    if not 3 <= len(cids) <= 8:
        warn(f"Unusual number of criteria ({len(cids)}), 4-7 is best")
    total = sum(c.get("weight", 0) for c in d["criteria"])
    if total != 100:
        warn(f"Weights add up to {total}, not 100 (the sheet normalizes them)")

    sids = set()
    for s in d["sources"]:
        sid = s.get("id")
        if not sid or sid in sids:
            err(f"Source with missing or duplicate id: {sid}")
        sids.add(sid)
        if s.get("type") not in SOURCE_TYPES:
            err(f"Source {sid}: invalid type '{s.get('type')}'")
        if s.get("independence") not in INDEPENDENCE:
            err(f"Source {sid}: invalid independence '{s.get('independence')}'")
        if not s.get("title"):
            err(f"Source {sid}: missing title")
        check_url(s.get("url"), f"source {sid}")
        check_date(s.get("date"), f"source {sid}")
    if not meta.get("example") and sum(1 for s in d["sources"] if s.get("independence") == "high") < 2:
        warn("Fewer than 2 high-independence sources: state this in 'limits'")

    pids = []
    for p in d["products"]:
        pid = p.get("id")
        pids.append(pid)
        if not pid or not p.get("name"):
            err(f"Product without id or name: {pid}")
            continue
        sc = p.get("scores", {})
        for cid in cids:
            v = sc.get(cid)
            if v is None:
                err(f"Product {pid}: missing score for criterion '{cid}'")
            elif not isinstance(v, (int, float)) or isinstance(v, bool) or not 0 <= v <= 10:
                err(f"Product {pid}: score '{cid}' out of range 0-10 ({v})")
        if set(sc) - set(cids):
            warn(f"Product {pid}: scores for unknown criteria: {sorted(set(sc) - set(cids))}")
        if p.get("data_confidence") not in CONFIDENCE:
            err(f"Product {pid}: invalid data_confidence '{p.get('data_confidence')}'")
        for s in p.get("sources", []):
            if s not in sids:
                err(f"Product {pid}: unknown source '{s}'")
        if not p.get("pros") or not p.get("cons"):
            warn(f"Product {pid}: add at least one pro and one con")
        if p.get("official_url"):
            check_url(p["official_url"], f"product {pid} official_url", required=False)
        offers = p.get("offers", [])
        if not offers:
            warn(f"Product {pid}: no offers, the sheet will show 'price not verified'")
        verified = 0
        for i, o in enumerate(offers):
            w = f"product {pid}, offer {i + 1}"
            if not o.get("store"):
                err(f"{w}: missing store")
            check_url(o.get("url"), w)
            check_date(o.get("date"), w, required=o.get("price") is not None)
            if o.get("price") is not None:
                if not isinstance(o["price"], (int, float)) or o["price"] <= 0:
                    err(f"{w}: invalid price")
                elif o.get("verified") is not False:
                    verified += 1
        if offers and not verified:
            warn(f"Product {pid}: no offer with a verified price")
    if len(set(pids)) != len(pids):
        err("Duplicate product ids")
    if not 2 <= len(pids) <= 8:
        warn(f"Unusual number of products ({len(pids)})")

    for g in d["feature_groups"]:
        for r in g.get("rows", []):
            lab = r.get("label", "?")
            if r.get("best", "none") not in BEST:
                err(f"Row '{lab}': invalid 'best' value")
            vals = r.get("values", {})
            for pid in pids:
                if pid not in vals:
                    warn(f"Row '{lab}': missing value for {pid} (shown as n/a)")
            for pid in vals:
                if pid not in pids:
                    err(f"Row '{lab}': unknown product '{pid}'")
            src = r.get("source", [])
            for s in ([src] if isinstance(src, str) else src):
                if s not in sids:
                    err(f"Row '{lab}': unknown source '{s}'")
            if r.get("best") in ("high", "low"):
                for pid, v in vals.items():
                    n = v.get("n") if isinstance(v, dict) else v
                    if v is not None and not isinstance(n, (int, float)):
                        warn(f"Row '{lab}': non-numeric value for {pid}, it cannot be highlighted")

    pk = d["pick"]
    if pk.get("product_id") not in pids:
        err(f"pick.product_id is unknown: {pk.get('product_id')}")
    if not pk.get("reasons"):
        err("pick.reasons is missing")
    if not pk.get("not_for_you_if"):
        warn("pick.not_for_you_if is missing: say when another option is better")
    for a in pk.get("alternatives", []):
        if a.get("product_id") not in pids:
            err(f"Alternative with unknown product: {a.get('product_id')}")
    if not d.get("limits"):
        warn("No limits declared: is it true the research had none?")

    if meta.get("date") and DATE_RE.match(meta["date"]):
        try:
            age = (date.today() - date.fromisoformat(meta["date"])).days
            if age > 3 and not meta.get("example"):
                warn(f"meta.date is {age} days old: re-verify prices")
        except ValueError:
            pass


def build(d, out):
    tpl = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in tpl:
        raise SystemExit("Invalid template: data placeholder not found")
    payload = (
        json.dumps(d, ensure_ascii=False)
        .replace("</", "<\\/")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )
    page = tpl.replace(PLACEHOLDER, payload)
    page = re.sub(r"<title>.*?</title>", lambda _: f"<title>{html.escape(d['meta']['short_title'])}</title>", page, count=1, flags=re.S)
    page = page.replace("__DESCRIPTION__", html.escape(d["summary"][:200], quote=True))
    lang = d["meta"]["locale"].split("-")[0].lower()
    page = page.replace('<html lang="en">', f'<html lang="{html.escape(lang)}">', 1)
    Path(out).write_text(page, encoding="utf-8")


def run(src, out):
    """Validate and build. Returns (errors, warnings)."""
    errors.clear()
    warnings.clear()
    data = json.loads(Path(src).read_text(encoding="utf-8"))
    validate(data)
    if not errors:
        build(data, out)
    return list(errors), list(warnings)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    out = sys.argv[2] if len(sys.argv) > 2 else "comparison-sheet.html"
    try:
        errs, warns = run(sys.argv[1], out)
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: cannot read the JSON: {e}")
        return 1
    for w in warns:
        print(f"WARNING: {w}")
    if errs:
        for e in errs:
            print(f"ERROR: {e}")
        print(f"\n{len(errs)} error(s): sheet not generated.")
        return 1
    print(f"OK: sheet written to {out} ({len(warns)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
