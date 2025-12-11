import requests
import json
import os

url = "https://assets5.lottiefiles.com/packages/lf20_sufg7a.json"
try:
    print("Downloading Lottie JSON...")
    r = requests.get(url, timeout=10)
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
