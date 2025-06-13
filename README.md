# convertOfficialJ-CHAT

J-CHAT公式の書き起こしの形式を，J-Moshiのfine-tuning用の形式に直す．

```J-CHAT公式の書き起こしの形式
{
  "id": "2c1b6e23f7d3e8214f2c5807711f40a1",
  "start": 0,
  "duration": 4.590000000000032,
  "channel": 0,
  "supervisions": [
    {
      "id": "2c1b6e23f7d3e8214f2c5807711f40a1_505",
      "recording_id": "2c1b6e23f7d3e8214f2c5807711f40a1",
      "start": 0.0,
      "duration": 0.4049999999999727,
      "channel": 0,
      "text": null,
      "language": null,
      "speaker": "SPEAKER_00",
      "gender": null,
      "custom": null,
      "alignment": null
    },
    {
      "id": "2c1b6e23f7d3e8214f2c5807711f40a1_506",
      "recording_id": "2c1b6e23f7d3e8214f2c5807711f40a1",
      "start": 0.42200000000002547,
      "duration": 2.4809999999999945,
      "channel": 0,
      "text": null,
      "language": null,
      "speaker": "SPEAKER_02",
      "gender": null,
      "custom": null,
      "alignment": null
    },
    {
      "id": "2c1b6e23f7d3e8214f2c5807711f40a1_507",
      "recording_id": "2c1b6e23f7d3e8214f2c5807711f40a1",
      "start": 3.0710000000000264,
      "duration": 1.5190000000000055,
      "channel": 0,
      "text": null,
      "language": null,
      "speaker": "SPEAKER_00",
      "gender": null,
      "custom": null,
      "alignment": null
    },
    {
      "id": "2c1b6e23f7d3e8214f2c5807711f40a1-000000",
      "recording_id": "2c1b6e23f7d3e8214f2c5807711f40a1",
      "start": 2.86,
      "duration": 0.64,
      "channel": 0,
      "text": "うん",
      "language": "ja",
      "speaker": null,
      "gender": null,
      "custom": null,
      "alignment": null
    },
    {
      "id": "2c1b6e23f7d3e8214f2c5807711f40a1-000001",
      "recording_id": "2c1b6e23f7d3e8214f2c5807711f40a1",
      "start": 3.5,
      "duration": 0.24,
      "channel": 0,
      "text": "む",
      "language": "ja",
      "speaker": null,
      "gender": null,
      "custom": null,
      "alignment": null
    },
    {
      "id": "2c1b6e23f7d3e8214f2c5807711f40a1-000002",
      "recording_id": "2c1b6e23f7d3e8214f2c5807711f40a1",
      "start": 3.74,
      "duration": 0.16,
      "channel": 0,
      "text": "っちゃ",
      "language": "ja",
      "speaker": null,
      "gender": null,
      "custom": null,
      "alignment": null
    },
    {
      "id": "2c1b6e23f7d3e8214f2c5807711f40a1-000003",
      "recording_id": "2c1b6e23f7d3e8214f2c5807711f40a1",
      "start": 3.9,
      "duration": 0.24,
      "channel": 0,
      "text": "いい",
      "language": "ja",
      "speaker": null,
      "gender": null,
      "custom": null,
      "alignment": null
    },
    {
      "id": "2c1b6e23f7d3e8214f2c5807711f40a1-000004",
      "recording_id": "2c1b6e23f7d3e8214f2c5807711f40a1",
      "start": 4.14,
      "duration": 0.16,
      "channel": 0,
      "text": "や",
      "language": "ja",
      "speaker": null,
      "gender": null,
      "custom": null,
      "alignment": null
    },
    {
      "id": "2c1b6e23f7d3e8214f2c5807711f40a1-000005",
      "recording_id": "2c1b6e23f7d3e8214f2c5807711f40a1",
      "start": 4.3,
      "duration": 0.08,
      "channel": 0,
      "text": "ん",
      "language": "ja",
      "speaker": null,
      "gender": null,
      "custom": null,
      "alignment": null
    },
    {
      "id": "2c1b6e23f7d3e8214f2c5807711f40a1-000006",
      "recording_id": "2c1b6e23f7d3e8214f2c5807711f40a1",
      "start": 4.38,
      "duration": 0.21002268,
      "channel": 0,
      "text": "。",
      "language": "ja",
      "speaker": null,
      "gender": null,
      "custom": null,
      "alignment": null
    }
  ]
}
```

```J-Moshiのfine-tuning用の形式
[
   {"speaker": "B", "word": "うん", "start": 2.86, "end": 3.5},
   {"speaker": "A", "word": "む", "start": 3.5, "end": 3.74},
   {"speaker": "A", "word": "っちゃ", "start": 3.74, "end": 3.9},
   {"speaker": "A", "word": "いい", "start": 3.9, "end": 4.14},
   {"speaker": "A", "word": "や", "start": 4.14, "end": 4.3},
   {"speaker": "A", "word": "ん", "start": 4.3, "end": 4.38},
   {"speaker": "B", "word": "。", "start": 4.38, "end": 4.59}
]
```