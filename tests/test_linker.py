import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from linker import NoteLinker, SAMPLE_NOTES, tokenize  # noqa: E402


class TestLinker(unittest.TestCase):
    def setUp(self):
        self.l = NoteLinker()
        for name, text in SAMPLE_NOTES.items():
            self.l.add_note(name, text)

    def test_suggest_runs(self):
        s = self.l.suggest(top_k=2)
        self.assertEqual(set(s.keys()), set(SAMPLE_NOTES.keys()))

    def test_related_notes_linked(self):
        s = self.l.suggest(top_k=2, min_score=0.05)
        targets = [l.target for l in s["向量检索"]]
        # 向量检索 与 余弦相似度 高度相关
        self.assertIn("余弦相似度", targets)

    def test_unrelated_notes_not_linked(self):
        s = self.l.suggest(top_k=4, min_score=0.15)
        breakfast_targets = [l.target for l in s["早餐"]]
        # 早餐与技术笔记无明显共享术语
        self.assertNotIn("向量检索", breakfast_targets)

    def test_no_self_link(self):
        s = self.l.suggest(top_k=4)
        for note, links in s.items():
            for l in links:
                self.assertNotEqual(l.source, l.target)

    def test_topk_limit(self):
        s = self.l.suggest(top_k=1)
        for links in s.values():
            self.assertLessEqual(len(links), 1)

    def test_empty(self):
        self.assertEqual(NoteLinker().suggest(), {})

    def test_tokenize_bigram(self):
        toks = tokenize("向量检索")
        self.assertIn("向量", toks)
        self.assertIn("量检", toks)


if __name__ == "__main__":
    unittest.main()
