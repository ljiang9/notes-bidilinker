# notes-bidilinker

零第三方依赖的笔记自动双链：基于术语共现与相似度，为一组笔记推荐应插入的 `[[双向链接]]`。

## 功能简介

- 把每篇笔记分词（中文二元组 + 英文成词，带轻量停用词）；
- 两两计算词袋余弦相似度；
- 超过阈值的笔记对互相成为候选双链，为每篇取 top-k；
- 输出可直接粘贴到笔记里的 `[[笔记名]]` 建议与对应相似度。

## 快速开始

```bash
python3 cli.py
```

代码调用：

```python
from linker import NoteLinker
l = NoteLinker()
l.add_note("我的笔记A", "笔记内容……")
l.add_note("我的笔记B", "笔记内容……")
suggest = l.suggest(top_k=2)  # {笔记名: [Link(source, target, score), ...]}
```

## 无 API key 如何运行

本项目**完全不需要 API key**，相似度计算与双链推荐全部本地完成。

## 目录说明

```
notes-bidilinker/
├── linker.py             # 核心库：NoteLinker / Link / tokenize
├── cli.py                # 命令行入口（内置样例笔记）
├── tests/test_linker.py  # unittest 测试
└── README.md
```

## 运行测试

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT License，Copyright (c) 2026 ljiang9
