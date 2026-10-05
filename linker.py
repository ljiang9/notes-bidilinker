"""linker.py — 笔记自动双链建议（零第三方依赖）。

基于术语共现 + 向量相似度，为一组笔记两两打分，给每篇笔记推荐
应插入的 [[双向链接]]。相似度高的笔记互相成为候选双链。
"""
from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

_TOKEN_RE = re.compile(r"[A-Za-z0-9]+|[\u4e00-\u9fff]+")
_STOP = {"的", "了", "和", "与", "是", "在", "我们", "这", "那", "the", "a", "an", "of"}


def tokenize(text: str) -> List[str]:
    out: List[str] = []
    for m in _TOKEN_RE.findall(text.lower()):
        if re.match(r"[\u4e00-\u9fff]", m):
            grams = [m[i:i + 2] for i in range(len(m) - 1)] if len(m) > 1 else [m]
            out.extend(g for g in grams if g not in _STOP)
        elif m not in _STOP:
            out.append(m)
    return out


@dataclass
class Link:
    source: str
    target: str
    score: float


class NoteLinker:
    def __init__(self) -> None:
        self.notes: Dict[str, Counter] = {}

    def add_note(self, name: str, text: str) -> None:
        self.notes[name] = Counter(tokenize(text))

    @staticmethod
    def _cos(a: Counter, b: Counter) -> float:
        if not a or not b:
            return 0.0
        dot = sum(c * b.get(t, 0) for t, c in a.items())
        na = math.sqrt(sum(c * c for c in a.values()))
        nb = math.sqrt(sum(c * c for c in b.values()))
        return dot / (na * nb) if na and nb else 0.0

    def suggest(self, top_k: int = 2, min_score: float = 0.05) -> Dict[str, List[Link]]:
        """为每篇笔记返回 top-k 条双链建议（不含自身，按分数降序）。"""
        names = list(self.notes.keys())
        result: Dict[str, List[Link]] = {n: [] for n in names}
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                score = self._cos(self.notes[a], self.notes[b])
                if score < min_score:
                    continue
                result[a].append(Link(a, b, score))
                result[b].append(Link(b, a, score))
        for n in names:
            result[n].sort(key=lambda l: l.score, reverse=True)
            result[n] = result[n][:top_k]
        return result


# 内置样例笔记。
SAMPLE_NOTES: Dict[str, str] = {
    "向量检索": "向量检索把文本映射到高维空间，用余弦相似度召回最相似的文档片段。",
    "余弦相似度": "余弦相似度衡量两个向量夹角，对长度不敏感，常用于向量检索排序。",
    "早餐": "早上吃了豆浆油条，还散了步，天气很好。",
    "混合检索": "BM25 关键词召回加向量精排，兼顾精确匹配和语义泛化。",
}
