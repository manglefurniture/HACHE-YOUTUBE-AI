import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("plan_shorts_batch", ROOT / "scripts/plan_shorts_batch.py")
planner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(planner)


class PlannerTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(planner.DEFAULT.read_text(encoding="utf-8"))

    def test_complete_series(self):
        result = planner.plan(self.data, None)
        self.assertEqual(len(result["episodes"]), 10)
        self.assertEqual(len(result["jobs"]), 90)
        self.assertEqual(result["vidiq_credits"], 0)
        self.assertFalse(result["execution_enabled"])
        self.assertEqual(result["provider_calls"], 0)

    def test_batches_and_dependencies(self):
        for batch, first in (("A", "S04"), ("B", "S09")):
            result = planner.plan(self.data, batch)
            self.assertEqual(result["episodes"][0], first)
            self.assertEqual(len(result["jobs"]), 45)
            ids = {j["id"] for j in result["jobs"]}
            self.assertEqual(len(ids), 45)
            for job in result["jobs"]:
                self.assertTrue(set(job["depends_on"]) <= ids)
                self.assertEqual(job["status"], "ready_for_research" if job["stage"] == "research" else "blocked")
                if job["stage"] == "publication":
                    self.assertTrue(job["approval_required"])

    def test_reject_spend_and_publish(self):
        for key in ("paid_generation", "gpu_rental", "publication"):
            data = copy.deepcopy(self.data)
            data["policy"]["authorization"][key] = True
            with self.assertRaises(ValueError):
                planner.plan(data, None)
        self.data["research"]["credit_budget"] = 1
        with self.assertRaises(ValueError):
            planner.plan(self.data, None)

    def test_invalid_batch_and_duplicate(self):
        with self.assertRaises(ValueError):
            planner.plan(self.data, "missing")
        self.data["batches"][1]["episode_ids"][0] = "S04"
        with self.assertRaises(ValueError):
            planner.plan(self.data, None)

    def test_unknown_source(self):
        self.data["episodes"][0]["source_ids"].append("missing")
        with self.assertRaises(ValueError):
            planner.plan(self.data, None)


if __name__ == "__main__":
    unittest.main()
