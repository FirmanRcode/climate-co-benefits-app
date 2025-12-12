import requests
import json
import os

# Reliable "Growing Plant" Lottie URL
LOTTIE_URL = "https://assets5.lottiefiles.com/packages/lf20_zprb9voq.json"

save_path = "assets/lottie_nature.json"

# Ensure assets directory exists
os.makedirs("assets", exist_ok=True)

print(f"Downloading Lottie animation from {LOTTIE_URL}...")
try:
    response = requests.get(LOTTIE_URL, timeout=10)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"Success! Saved to {save_path} (Size: {len(response.content)} bytes)")
    else:
        print(f"Failed to download. Status code: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")
