import requests
import json
import os

# Reliable "Money/Plant Growth" Lottie URL
# This is a high quality 'Investment Growth' animation similar to the request
LOTTIE_URL = "https://assets10.lottiefiles.com/packages/lf20_tijmpkyq.json" 

# Headers to mimic a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

save_path = "assets/lottie_nature.json"

# Ensure assets directory exists
os.makedirs("assets", exist_ok=True)

print(f"Downloading Lottie animation from {LOTTIE_URL}...")
try:
    response = requests.get(LOTTIE_URL, headers=HEADERS, timeout=10)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"Success! Saved to {save_path} (Size: {len(response.content)} bytes)")
    else:
        print(f"Failed to download. Status code: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")
