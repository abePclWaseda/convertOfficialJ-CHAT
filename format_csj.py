import json
import re
from pathlib import Path

# ====== 設定 ======
IN_PATH = Path("/mnt/aoni01/db/CSJ/CSJ2004/SPEECH/D02F0015/D02F0015.sdb")  # 入力 SDB
OUT_PATH = Path(
    "/mnt/kiso-qnap3/yuabe/m1/convertOfficialJ-CHAT/data/CSJ/D02F0015.json"
)  # 出力 JSON
CHANNEL2SPK = {"L": "A", "R": "B"}  # チャネル→話者マッピング
time_pat = re.compile(r"(\d{5}\.\d+)-(\d{5}\.\d+)")  # 00000.341-00001.020
chan_pat = re.compile(r"\b([LR]):")  # L:-001-001 など

transcript = []

with IN_PATH.open(encoding="shift_jis") as f:
    for line in f:
        cols = line.rstrip("\n").split("\t")
        if len(cols) < 7:  # 形態素列が無い行はスキップ
            continue

        # --- 開始/終了秒 ---
        m_t = time_pat.search(cols[3])
        if not m_t:
            continue
        start, end = map(float, m_t.groups())

        # --- チャネル → スピーカー ---
        m_c = chan_pat.search(cols[3])
        speaker = CHANNEL2SPK.get(m_c.group(1), "?") if m_c else "?"

        # --- 語表層形（列 7 以降の先頭） ---
        word = cols[7].strip()

        transcript.append(
            {
                "speaker": speaker,
                "word": word,
                "start": start,
                "end": end,
            }
        )

# JSON 出力
with OUT_PATH.open("w", encoding="utf-8") as f:
    json.dump(transcript, f, ensure_ascii=False, indent=2)

print(f"✔ 変換完了 → {OUT_PATH}")
