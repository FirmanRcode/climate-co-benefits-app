import requests
import json
import os

# GitHub Raw URL (High Reliability)
# This is a 'Growth/Success' animation from a public repo
LOTTIE_URL = "https://raw.githubusercontent.com/thesvbd/Lottie-examples/master/assets/animations/loading.json" 
# Backup: https://raw.githubusercontent.com/airbnb/lottie-android/master/lottie/src/main/res/raw/bullseye.json
# Note: Specific 'Money Growth' might be hard to find on raw github, using a generic 'Loading/Growth' one for now to fix the 403.

save_path = "assets/lottie_nature.json"

# Ensure assets directory exists
os.makedirs("assets", exist_ok=True)

print(f"Downloading Lottie animation from {LOTTIE_URL}...")
try:
    response = requests.get(LOTTIE_URL, timeout=10) # No headers needed for GitHub Raw usually
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"Success! Saved to {save_path} (Size: {len(response.content)} bytes)")
    else:
        print(f"Failed to download. Status code: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")

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
