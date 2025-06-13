import json


def load_supervisions(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["supervisions"]


def build_speaker_segments(supervisions):
    return [
        {
            "speaker": "A" if sup["speaker"] == "SPEAKER_00" else "B",
            "start": sup["start"],
            "end": sup["start"] + sup["duration"],
        }
        for sup in supervisions
        if sup.get("speaker") is not None and sup.get("text") is None
    ]


def assign_speaker_to_transcripts(supervisions, speaker_segments):
    transcripts = [sup for sup in supervisions if sup.get("text") is not None]
    results = []
    for seg in transcripts:
        seg_start = seg["start"]
        seg_end = seg["start"] + seg["duration"]
        speaker = "B"
        for spk_seg in speaker_segments:
            if spk_seg["start"] <= seg_start and seg_end <= spk_seg["end"]:
                speaker = spk_seg["speaker"]
                break
        results.append(
            {
                "speaker": speaker,
                "word": seg["text"],
                "start": round(seg_start, 3),
                "end": round(seg_end, 3),
            }
        )
    return results


def convert_and_write_list(json_path, output_path):
    supervisions = load_supervisions(json_path)
    speaker_segments = build_speaker_segments(supervisions)
    word_level = assign_speaker_to_transcripts(supervisions, speaker_segments)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("[\n")
        for i, item in enumerate(word_level):
            comma = "," if i < len(word_level) - 1 else ""
            f.write("   " + json.dumps(item, ensure_ascii=False) + comma + "\n")
        f.write("]\n")


# 使い方
convert_and_write_list(
    "/mnt/work-qnap/llmc/J-CHAT/text/podcast_test/00000-of-00001/cuts.000000/2c1b6e23f7d3e8214f2c5807711f40a1.json",
    "output.json",
)
