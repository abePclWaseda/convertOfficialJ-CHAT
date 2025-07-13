#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Convert CHAT (.cha) file to flat JSON.

Usage:
    python cha2json.py 0696.cha 0696.json
    python convert_callhome.py /mnt/work-qnap/llmc/jpn/0696.cha data/CallHome/0696.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

# ---- 正規表現パターン ----
UTTER_RE = re.compile(
    r"^\*([A-Za-z]):\s*(.+?)\s*\x15(\d+)_(\d+)\x15"
)  # 話者・内容・開始ms・終了ms
BRACKETS_RM = re.compile(
    r"\[:[^]]*]|&=[A-Za-z]+|\{[^}]*}|<[^>]*>|◉|⁇|⇗|⇘"
)  # 注釈や記号の削除


def load_cha(path: Path) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []

    with path.open(encoding="utf-8") as f:
        for line in f:
            m = UTTER_RE.match(line)
            if not m:
                continue

            spk, utt, start_ms, end_ms = m.groups()
            start_ms, end_ms = int(start_ms), int(end_ms)

            # 注釈類の粗削除
            utt_clean = BRACKETS_RM.sub("", utt)
            words = [w for w in utt_clean.split() if w]

            # 単語数で均等割り（単語境界時刻が無い .cha の場合の近似）
            if words:
                dur = (end_ms - start_ms) / 1000.0
                w_len = dur / len(words)
                for i, w in enumerate(words):
                    rec = {
                        "speaker": spk,
                        "word": w,
                        "start": round(start_ms / 1000.0 + i * w_len, 3),
                        "end": round(start_ms / 1000.0 + (i + 1) * w_len, 3),
                    }
                    records.append(rec)

    return records


def main(src: str, dst: str) -> None:
    items = load_cha(Path(src))
    with Path(dst).open("w", encoding="utf-8") as f:
        pad = " " * 3  # 3 スペースのインデント
        f.write("[\n")
        for i, obj in enumerate(items):
            line = pad + json.dumps(obj, ensure_ascii=False, separators=(",", ": "))
            if i != len(items) - 1:
                line += ","
            f.write(line + "\n")
        f.write("]\n")
    print(f"✔ JSON written to {dst}  ({len(items)} records)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python cha2json.py INPUT.cha OUTPUT.json")
    main(sys.argv[1], sys.argv[2])
