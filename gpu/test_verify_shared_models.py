import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("verify_shared_models", Path(__file__).with_name("verify-shared-models.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class VerifyModelsTests(unittest.TestCase):
    def test_missing_models_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            result = module.verify(Path(directory), False)
            self.assertTrue(result)
            self.assertTrue(all(value == "missing" for value in result.values()))

    def test_present_and_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in module.MODELS:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"test")
            self.assertTrue(all(v == "present_unverified" for v in module.verify(root, False).values()))
            self.assertTrue(all(v == "hash_mismatch" for v in module.verify(root, True).values()))

if __name__ == "__main__":
    unittest.main()
