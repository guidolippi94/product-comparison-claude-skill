"""Basic tests for the validator and the sheet builder. Run: python -m unittest discover tests"""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "product-comparison" / "scripts"))
import build_sheet  # noqa: E402

EXAMPLE = ROOT / "product-comparison" / "assets" / "example-data.json"


class BuildTests(unittest.TestCase):
    def run_data(self, data):
        with tempfile.TemporaryDirectory() as tmp:
            src, out = Path(tmp) / "d.json", Path(tmp) / "o.html"
            src.write_text(json.dumps(data), encoding="utf-8")
            errs, warns = build_sheet.run(src, out)
            html = out.read_text(encoding="utf-8") if out.exists() else ""
        return errs, warns, html

    def example(self):
        return json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_example_builds(self):
        errs, _, html = self.run_data(self.example())
        self.assertEqual(errs, [])
        self.assertIn("<title>Robot vacuums</title>", html)
        self.assertIn('<html lang="en">', html)
        self.assertNotIn("/*__DATA__*/", html)

    def test_locale_sets_lang(self):
        d = self.example()
        d["meta"]["locale"] = "it-IT"
        d["meta"]["currency"] = "EUR"
        _, _, html = self.run_data(d)
        self.assertIn('<html lang="it">', html)

    def test_rejects_affiliate_params(self):
        d = self.example()
        d["products"][0]["offers"][0]["url"] = "https://www.example.com/p?tag=me-20&utm_source=x"
        errs, _, html = self.run_data(d)
        self.assertTrue(any("tracking" in e for e in errs))
        self.assertEqual(html, "")

    def test_rejects_http_and_short_links(self):
        d = self.example()
        d["products"][0]["offers"][0]["url"] = "http://www.example.com/p"
        d["products"][1]["offers"][0]["url"] = "https://amzn.to/abc"
        errs, _, _ = self.run_data(d)
        self.assertGreaterEqual(len(errs), 2)

    def test_score_out_of_range(self):
        d = self.example()
        d["products"][0]["scores"]["suction"] = 11
        errs, _, _ = self.run_data(d)
        self.assertTrue(any("out of range" in e for e in errs))

    def test_unknown_pick(self):
        d = self.example()
        d["pick"]["product_id"] = "nope"
        errs, _, _ = self.run_data(d)
        self.assertTrue(any("pick.product_id" in e for e in errs))

    def test_bad_currency_and_locale(self):
        d = self.example()
        d["meta"]["currency"] = "euro"
        d["meta"]["locale"] = "it_IT"
        errs, _, _ = self.run_data(d)
        self.assertEqual(sum(1 for e in errs if "meta." in e), 2)

    def test_script_tag_in_text_is_escaped(self):
        d = self.example()
        d["summary"] = "x </script><script>alert(1)</script>"
        errs, _, html = self.run_data(d)
        self.assertEqual(errs, [])
        self.assertNotIn("</script><script>alert(1)", html)


if __name__ == "__main__":
    unittest.main()
