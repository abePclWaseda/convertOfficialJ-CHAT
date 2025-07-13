import os
import requests
from tqdm import tqdm

# 保存先ディレクトリ
SAVE_DIR = "/mnt/work-qnap/llmc/CallHome/audio"
os.makedirs(SAVE_DIR, exist_ok=True)

# ダウンロード対象ID（必要に応じて拡張）
wav_ids = [
    "0696", "0743", "0856", "0862", "0922", "0924", "0930", "0986", "0988",
    "1003", "1005", "1012", "1032", "1041", "1048", "1057", "1069", "1072", "1099",
    "1109", "1123", "1201", "1237", "1263", "1277", "1288", "1290", "1328", "1369",
    "1370", "1418", "1425", "1428", "1461", "1509", "1538", "1541", "1542", "1557",
    "1586", "1593", "1604", "1607", "1608", "1615", "1622", "1628", "1629", "1642",
    "1667", "1670", "1674", "1688", "1690", "1710", "1713", "1725", "1731", "1738",
    "1741", "1749", "1832", "1867", "1889", "1899", "1925", "1928", "1966", "1967",
    "1999", "2004", "2035", "2041", "2053", "2074", "2085", "2096", "2111", "2134",
    "2157", "2180", "2188", "2196", "2199", "2204", "2206", "2207", "2208", "2209",
    "2210", "2212", "2214", "2215", "2216", "2217", "2218", "2219", "2220", "2222",
    "2223", "2224", "2225", "2231", "2234", "2235", "2236", "2237", "2238", "2239",
    "2242", "2243", "3001", "3002", "3004", "3005", "3006", "3007", "3008", "4061", "4275"
]

# Cookie の設定（ブラウザから取得）
cookies = {
    "talkbank": "s%3A0x2tkaXZwOnJEvzK1UIXCi9KaWaeFnwC.BfoDXd1tg67i3Kinkdkz0lFr4cBihRFHRu%2F3VhhKMEY"
}

# User-Agent（ブラウザに似せる）
headers = {"User-Agent": "Mozilla/5.0"}

# ベースURL
base_url = "https://media.talkbank.org/ca/CallHome/jpn/0wav"

# ダウンロードループ
for wav_id in tqdm(wav_ids):
    filename = f"{wav_id}.wav"
    url = f"{base_url}/{filename}?f=save"
    save_path = os.path.join(SAVE_DIR, filename)

    if os.path.exists(save_path):
        continue

    try:
        r = requests.get(url, headers=headers, cookies=cookies, stream=True, timeout=30)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
        tqdm.write(f"Downloaded: {filename}")
    except Exception as e:
        tqdm.write(f"Failed: {filename} - {e}")
