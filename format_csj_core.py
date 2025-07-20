import json
import re
from pathlib import Path

# ====== 設定 ======
IN_DIR = Path("/mnt/aoni01/db/CSJ/USB/MORPH/SDB/noncore/")
OUT_DIR = Path("./data/CSJ/noncore")  # 出力ディレクトリ（必要に応じて変更）
OUT_DIR.mkdir(exist_ok=True)

# 正規表現パターン
time_pat = re.compile(r"(\d{5}\.\d+)-(\d{5}\.\d+)")
chan_pat = re.compile(r"\b([LR]):")
channel_map = {"L": "A", "R": "B"}

# ====== 各 SDB ファイルを処理 ======
for sdb_path in sorted(IN_DIR.glob("D*.sdb")):
    transcript = []
    try:
        with sdb_path.open(encoding="shift_jis") as f:
            for line in f:
                cols = line.rstrip("\n").split("\t")
                if len(cols) < 8:
                    continue

                time_match = time_pat.search(cols[3])
                chan_match = chan_pat.search(cols[3])
                if not time_match or not chan_match:
                    continue

                start, end = map(float, time_match.groups())
                speaker = channel_map.get(chan_match.group(1), "?")
                word = cols[7].strip()

                transcript.append(
                    {
                        "speaker": speaker,
                        "word": word,
                        "start": round(start, 3),
                        "end": round(end, 3),
                    }
                )

        # JSON 出力ファイル名
        out_path = OUT_DIR / (sdb_path.stem + ".json")
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(transcript, f, ensure_ascii=False, indent=2)

        print(f"✔ Processed: {sdb_path.name} → {out_path.name}")

    except Exception as e:
        print(f"✖ Error in {sdb_path.name}: {e}")
