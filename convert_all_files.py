import os
import json
from tqdm import tqdm


def load_supervisions(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["supervisions"]


def build_speaker_segments(supervisions):
    # 全 speaker ID を順に取得
    speaker_ids = [
        sup["speaker"]
        for sup in supervisions
        if sup.get("text") is None and sup.get("speaker") is not None
    ]
    # 最初に現れた話者を "A" とする
    primary_speaker = speaker_ids[0] if speaker_ids else None

    segments = []
    for sup in supervisions:
        if sup.get("text") is None and sup.get("speaker") is not None:
            role = "A" if sup["speaker"] == primary_speaker else "B"
            segments.append(
                {
                    "speaker": role,
                    "start": sup["start"],
                    "end": sup["start"] + sup["duration"],
                }
            )
    return segments


def assign_speaker_to_words(supervisions, speaker_segments):
    word_segs = []
    for seg in supervisions:
        if seg.get("text") is None:
            continue
        seg_start = seg["start"]
        seg_end = seg["start"] + seg["duration"]
        speaker = "B"
        for spk in speaker_segments:
            if spk["start"] <= seg_start and seg_end <= spk["end"]:
                speaker = spk["speaker"]
                break
        word_segs.append(
            {
                "speaker": speaker,
                "word": seg["text"],
                "start": round(seg_start, 3),
                "end": round(seg_end, 3),
            }
        )
    return word_segs


def process_all_jsons(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    files = [f for f in os.listdir(input_dir) if f.endswith(".json")]

    for fname in tqdm(files, desc="Processing"):
        in_path = os.path.join(input_dir, fname)
        out_path = os.path.join(output_dir, fname)

        try:
            supervisions = load_supervisions(in_path)
            speaker_segments = build_speaker_segments(supervisions)
            words = assign_speaker_to_words(supervisions, speaker_segments)

            speaker_set = set(word["speaker"] for word in words)
            if speaker_set == {"A"} or speaker_set == {"B"}:
                print(f"🔎 Only one speaker ({list(speaker_set)[0]}) in file: {fname}")

            with open(out_path, "w", encoding="utf-8") as f:
                f.write("[\n")
                for i, word in enumerate(words):
                    comma = "," if i < len(words) - 1 else ""
                    f.write("   " + json.dumps(word, ensure_ascii=False) + comma + "\n")
                f.write("]\n")

        except Exception as e:
            print(f"Error processing {fname}: {e}")


# 🔧 使用例
process_all_jsons(
    input_dir="/mnt/work-qnap/llmc/J-CHAT/text/podcast_test/00000-of-00001/cuts.000000",
    output_dir="text_formatted",
)
