#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Batch-convert every .cha in a directory tree to JSON.

Usage examples
--------------
# 1) 同一フォルダに出力（従来と同じ）
python cha2json_batch.py /mnt/work-qnap/llmc/jpn

# 2) 出力先を指定（構造を保持して /tmp/json に保存）
python cha2json_batch.py /mnt/work-qnap/llmc/jpn --out /tmp/json -j 4
python cha2json.py /mnt/work-qnap/llmc/jpn --out /mnt/work-qnap/llmc/CallHome/text -j 4
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import re
from pathlib import Path
from typing import Any, Dict, List

# ---------- 1. .cha 1 件 → list[dict] ----------

UTTER_RE = re.compile(r"^\*([A-Za-z]):\s*(.+?)\s*\x15(\d+)_(\d+)\x15")
BRACKETS_RM = re.compile(r"\[:[^]]*]|&=[A-Za-z]+|\{[^}]*}|<[^>]*>|◉|⁇|⇗|⇘")

def load_cha(path: Path) -> List[Dict[str, Any]]:
    recs: List[Dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            m = UTTER_RE.match(line)
            if not m:
                continue
            spk, txt, s, e = m.groups()
            s_ms, e_ms = int(s), int(e)

            txt = BRACKETS_RM.sub("", txt)
            words = [w for w in txt.split() if w]
            if not words:
                continue

            dur = (e_ms - s_ms) / 1000.0
            step = dur / len(words)
            for i, w in enumerate(words):
                recs.append(
                    {
                        "speaker": spk,
                        "word": w,
                        "start": round(s_ms / 1000.0 + i * step, 3),
                        "end":   round(s_ms / 1000.0 + (i + 1) * step, 3),
                    }
                )
    return recs

def write_json(items: List[Dict[str, Any]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pad = " " * 3
    with out_path.open("w", encoding="utf-8") as f:
        f.write("[\n")
        for i, obj in enumerate(items):
            line = pad + json.dumps(obj, ensure_ascii=False, separators=(",", ": "))
            if i != len(items) - 1:
                line += ","
            f.write(line + "\n")
        f.write("]\n")

# ---------- 2. ワーカー ----------

def _process_one(args: tuple[Path, Path, Path]) -> str:
    cha_path, root_in, root_out = args
    rel = cha_path.relative_to(root_in)
    out_path = (root_out / rel).with_suffix(".json")
    items = load_cha(cha_path)
    write_json(items, out_path)
    return f"{cha_path.name} → {out_path.relative_to(root_out)} ({len(items)} rec)"

# ---------- 3. メイン ----------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("root_in", help="入力ディレクトリ（再帰的に .cha を検索）")
    ap.add_argument("-o", "--out", dest="root_out",
                    help="出力先ルート（省略時は入力と同じフォルダ）")
    ap.add_argument("-j", type=int, metavar="N", default=1,
                    help="並列ワーカー数 (デフォルト 1)")
    args = ap.parse_args()

    root_in = Path(args.root_in).expanduser().resolve()
    root_out = Path(args.root_out).expanduser().resolve() if args.root_out else root_in
    cha_files = sorted(root_in.rglob("*.cha"))
    if not cha_files:
        raise SystemExit("⚠ .cha ファイルが見つかりません")

    print(f"Found {len(cha_files)} .cha files under {root_in}")
    if root_out != root_in:
        print(f"JSON will be written under {root_out} (keeping relative paths)")

    # 並列処理用にタプルで渡す
    tasks = [(p, root_in, root_out) for p in cha_files]

    if args.j > 1:
        with mp.Pool(args.j) as pool:
            for msg in pool.imap_unordered(_process_one, tasks):
                print(msg)
    else:
        for t in tasks:
            print(_process_one(t))

    print("✔ All done.")

if __name__ == "__main__":
    main()
