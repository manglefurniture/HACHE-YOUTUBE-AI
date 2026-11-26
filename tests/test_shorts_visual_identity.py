import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("visual_preflight", ROOT / "scripts/check_shorts_visual_identity.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class VisualIdentityTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(module.DEFAULT.read_text(encoding="utf-8"))

    def test_current_profiles(self):
        self.assertEqual(module.validate(self.data), 5)

    def test_duplicate_face(self):
        first, second = self.data["episodes"][:2]
        second["visual_identity"]["human"]["face"] = first["visual_identity"]["human"]["face"].upper()
        with self.assertRaises(ValueError):
            module.validate(self.data)

    def test_wrong_id(self):
        self.data["episodes"][1]["visual_identity"]["human"]["id"] = "S04-H01"
        with self.assertRaises(ValueError):
            module.validate(self.data)

    def test_duplicate_robot_and_setting(self):
        for field in ("robot", "setting"):
            data = copy.deepcopy(self.data)
            a, b = data["episodes"][:2]
            if field == "robot":
                b["visual_identity"]["robot"]["design"] = a["visual_identity"]["robot"]["design"]
            else:
                b["visual_identity"]["setting"] = a["visual_identity"]["setting"]
            with self.assertRaises(ValueError):
                module.validate(data)

    def test_no_false_approval(self):
        self.data["episodes"][0]["visual_identity"]["historical_visual_review"] = "approved"
        with self.assertRaises(ValueError):
            module.validate(self.data)


if __name__ == "__main__":
    unittest.main()
