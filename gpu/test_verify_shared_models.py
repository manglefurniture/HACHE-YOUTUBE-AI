import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
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

    def test_image_only_verification_skips_unneeded_video_models(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            image = root / "checkpoints/juggernautXL_ragnarok.safetensors"
            image.parent.mkdir(parents=True)
            image.write_bytes(b"not-original-model")
            results = module.verify(root, False, only="juggernaut")
            self.assertEqual(results, {"checkpoints/juggernautXL_ragnarok.safetensors": "present_unverified"})
            self.assertEqual(module.verify(root, True, only="juggernaut")[image.relative_to(root).as_posix()], "hash_mismatch")
            self.assertEqual(len(module.verify(root, False)), 9)

if __name__ == "__main__":
    unittest.main()
