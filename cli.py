#!/usr/bin/env python3
"""cli.py — notes-bidilinker 命令行入口。

用法：python3 cli.py

在内置样例笔记上计算两两相似度，输出每篇笔记建议插入的 [[双链]]。
"""
from __future__ import annotations

import sys

from linker import SAMPLE_NOTES, NoteLinker


def main(argv=None) -> int:
    linker = NoteLinker()
    for name, text in SAMPLE_NOTES.items():
        linker.add_note(name, text)

    suggestions = linker.suggest(top_k=2)
    print("建议的 [[双向链接]]：\n")
    for note, links in suggestions.items():
        if not links:
            print(f"- {note}：（无相关笔记）")
            continue
        rendered = " ".join(f"[[{l.target}]]" for l in links)
        detail = ", ".join(f"[[{l.target}]]({l.score:.2f})" for l in links)
        print(f"- {note} → {rendered}")
        print(f"    相似度：{detail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
