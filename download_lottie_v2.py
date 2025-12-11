import requests
import json
import os

# Alternate URL (Plant Growing)
url = "https://lottie.host/5b09462c-f370-4f51-b02c-49d290687352/8Q3u4u2b52.json"

try:
    print(f"Downloading Lottie JSON from {url}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers, timeout=10)
    
    if r.status_code == 200:
        if not os.path.exists("assets"):
            os.makedirs("assets")
        with open("assets/lottie_nature.json", "w") as f:
            json.dump(r.json(), f)
        print("Success: Saved to assets/lottie_nature.json")
    else:
        print(f"Failed: Status {r.status_code}")
except Exception as e:
    print(f"Error: {e}")
