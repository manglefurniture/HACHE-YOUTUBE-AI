import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_shorts_timing as timing


def fixture():
    sections = {"hook":"Robots en casa.", "fact":"Un avance real.", "transition":"Imaginemos el futuro.",
                "fiction":"Nora vuelve.", "closing":"¿Qué opinas?"}
    text = "\n\n".join(sections.values())
    words = [{"text": t,"start": i*0.4,"end": i*0.4+0.3} for i,t in enumerate(text.split())]
    data = {"episode":"S04","script_sections":sections,"brand_close_seconds":2.6,
            "narration":{"duration_s":5.5},"transcript":{"generation_id":"fixture","text":text,"words":words}}
    specs = {"episodes":{"S04":[{"section":k,"anchor":v,"visual":k,"technique":"cpu"} for k,v in sections.items()]}}
    return data,specs


class TimingTests(unittest.TestCase):
    def test_real_intervals_and_brand(self):
        data,spec = fixture()
        srt,shots,report = timing.build(data,spec)
        self.assertIn("¿Qué opinas?", srt)
        self.assertEqual(shots[0]["start_s"], 0)
        self.assertEqual(shots[-1]["start_s"],5.5)
        self.assertEqual(shots[-1]["end_s"],8.1)
        self.assertTrue(all(a["end_s"]==b["start_s"] for a,b in zip(shots,shots[1:])))
        self.assertEqual(report["caption_count"],5)

    def test_rejects_transcript_change(self):
        data,spec = fixture()
        data["transcript"]["text"] += " Error."
        with self.assertRaises(ValueError):
            timing.build(data,spec)

    def test_rejects_missing_anchor(self):
        data,spec = fixture()
        spec["episodes"]["S04"][0]["anchor"]="inexistente"
        with self.assertRaises(ValueError):
            timing.build(data,spec)

    def test_rejects_excessive_timing(self):
        data,spec = fixture()
        data["transcript"]["words"][-1]["end"]=8
        with self.assertRaises(ValueError):
            timing.build(data,spec)

    def test_wrap(self):
        self.assertIsNotNone(timing.wrap(["Un","robot","experimental","aprende","una","tarea."]))
        self.assertIsNone(timing.wrap(["a"*28]))

    def test_clip_small_provider_discrepancy(self):
        data,spec = fixture()
        data["narration"]["duration_s"]=5.04
        _,shots,_=timing.build(data,spec)
        self.assertEqual(shots[-1]["start_s"],5.04)


if __name__ == "__main__":
    unittest.main()
