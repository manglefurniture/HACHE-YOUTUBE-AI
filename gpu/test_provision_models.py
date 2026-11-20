import hashlib
import io
import tempfile
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import provision_models as provision


class FakeBody(io.BytesIO):
    pass


class FakeR2:
    def __init__(self, data, fail_first=False):
        self.data = data
        self.calls = 0
        self.fail_first = fail_first

    def get_object(self, *, Bucket, Key):
        self.calls += 1
        if self.fail_first and self.calls == 1:
            raise OSError("temporary read failure")
        return {"Body": FakeBody(self.data), "ContentLength": len(self.data)}


class ProvisionModelsTests(unittest.TestCase):
    def test_inventory_has_nine_unique_public_models(self):
        bucket, models = provision.load_inventory()
        self.assertEqual(bucket, "hache-ai-models")
        self.assertEqual(len(models), 9)
        self.assertEqual(len({model["key"] for model in models}), 9)
        self.assertTrue(all(model["key"].startswith("shared/") for model in models))
        self.assertFalse(any("buffalo_l" in model["key"] for model in models))

    def test_download_streams_verifies_and_atomically_installs(self):
        data = b"public-model-bytes" * 100
        model = {
            "path": "checkpoints/example.bin",
            "key": "shared/example/example.bin",
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
        client = FakeR2(data)
        with tempfile.TemporaryDirectory() as temp:
            provision.download_one(client, "hache-ai-models", Path(temp), model)
            destination = Path(temp) / model["path"]
            self.assertEqual(destination.read_bytes(), data)
            self.assertFalse(destination.with_name("example.bin.part").exists())

    def test_retries_transient_r2_failure(self):
        data = b"retryable-data"
        model = {
            "path": "checkpoints/example.bin",
            "key": "shared/example/example.bin",
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
        client = FakeR2(data, fail_first=True)
        with tempfile.TemporaryDirectory() as temp, patch.object(provision.time, "sleep"):
            provision.download_one(client, "hache-ai-models", Path(temp), model)
            self.assertEqual(client.calls, 2)

    def test_matching_local_file_skips_r2(self):
        data = b"already-present"
        model = {
            "path": "checkpoints/example.bin",
            "key": "shared/example/example.bin",
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
        client = FakeR2(data)
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / model["path"]
            destination.parent.mkdir(parents=True)
            destination.write_bytes(data)
            provision.download_one(client, "hache-ai-models", Path(temp), model)
            self.assertEqual(client.calls, 0)

    def test_hash_mismatch_never_installs_file(self):
        data = b"wrong-content"
        model = {
            "path": "checkpoints/example.bin",
            "key": "shared/example/example.bin",
            "bytes": len(data),
            "sha256": hashlib.sha256(b"expected-content").hexdigest(),
        }
        with tempfile.TemporaryDirectory() as temp, patch.object(provision.time, "sleep"):
            with self.assertRaises(RuntimeError):
                provision.download_one(FakeR2(data), "hache-ai-models", Path(temp), model)
            self.assertFalse((Path(temp) / model["path"]).exists())


if __name__ == "__main__":
    unittest.main()
