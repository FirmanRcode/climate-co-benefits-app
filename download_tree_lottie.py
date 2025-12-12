import requests
import json
import os

# URL for a "Growing Tree" or Nature Lottie (Public URL)
# Using a reliable public source or a raw github link to a lottie file
# This is a 'Growing Plant' animation
LOTTIE_URL = "https://lottie.host/801a0d33-9118-471e-9242-7db60e31885b/9F6a16629K.json" 
# Alternative if above fails: https://assets2.lottiefiles.com/packages/lf20_4kji20Y9.json

save_path = "assets/lottie_nature.json"

# Ensure assets directory exists
os.makedirs("assets", exist_ok=True)

print(f"Downloading Lottie animation from {LOTTIE_URL}...")
try:
    response = requests.get(LOTTIE_URL)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Success! Saved to {save_path}")
    else:
        print(f"❌ Failed to download. Status code: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")
