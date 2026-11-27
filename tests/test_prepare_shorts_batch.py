import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import prepare_shorts_batch as prep


class PreparationTests(unittest.TestCase):
    def setUp(self):
        self.series = json.loads(prep.SERIES_DEFAULT.read_text(encoding="utf-8"))
        self.drafts = json.loads(prep.DEFAULT.read_text(encoding="utf-8"))

    def test_handoff_is_deterministic_and_offline(self):
        a = prep.build(self.series, self.drafts)
        self.assertEqual(a, prep.build(self.series, self.drafts))
        self.assertEqual((a["narration_jobs"], a["reference_jobs"]), (5, 10))
        self.assertEqual(a["provider_calls"], 0)
        self.assertFalse(a["execution_enabled"])
        self.assertEqual(len({j["narration"]["request_key"] for j in a["episodes"]}), 5)
        self.assertTrue(all(not j["narration"]["provider_called"] for j in a["episodes"]))
        self.assertTrue(all(e["canon_status"] == "proposed_unapproved" for e in a["universe"]))
        self.assertEqual(a["narration_characters"], sum(len(j["narration"]["request"]["text"]) for j in a["episodes"]))
        self.assertIn("S08", prep.review_markdown(a))

    def test_changed_script_changes_request_key(self):
        a = prep.build(self.series, self.drafts)
        changed = copy.deepcopy(self.drafts)
        changed["episodes"][0]["script"]["closing"] += " Comenta."
        changed["episodes"][0]["word_count"] += 1
        b = prep.build(self.series, changed)
        self.assertNotEqual(a["episodes"][0]["narration"]["request_key"], b["episodes"][0]["narration"]["request_key"])
        self.assertEqual(a["episodes"][1]["narration"]["request_key"], b["episodes"][1]["narration"]["request_key"])

    def test_rejects_wrong_batch_or_spend(self):
        for key in ("narration", "paid_generation", "gpu_rental", "publication"):
            d = copy.deepcopy(self.drafts)
            d["authorization"][key] = True
            with self.assertRaises(ValueError):
                prep.build(self.series, d)
        self.drafts["episodes"].reverse()
        with self.assertRaises(ValueError):
            prep.build(self.series, self.drafts)

    def test_rejects_unmapped_fact(self):
        self.drafts["episodes"][0]["facts"][0]["sources"] = ["missing"]
        with self.assertRaises(ValueError):
            prep.build(self.series, self.drafts)

    def test_write_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.json"
            prep.write_once(path, "same\n")
            prep.write_once(path, "same\n")
            with self.assertRaises(ValueError):
                prep.write_once(path, "changed\n")
            self.assertEqual(path.read_text(), "same\n")


if __name__ == "__main__":
    unittest.main()
