import requests
import os

# === CONFIG ===
BACKEND_URL = "http://127.0.0.1:5000/generate/image"
TEST_IMAGE_PATH = "test_assets/KakaoTalk_20250708_231845951.jpg"  # <-- Make sure this file exists
TEST_PARAMS = {
    "style": "8bit",
    "resolution": "32x32",
    "color_palette": "classic",
    "batch_count": "1"
}

# === RUN TEST ===
def test_generate_image():
    print(f"[🔍] Testing endpoint: {BACKEND_URL}")
    
    if not os.path.exists(TEST_IMAGE_PATH):
        print(f"[❌] Image not found at {TEST_IMAGE_PATH}")
        return
    
    try:
        with open(TEST_IMAGE_PATH, 'rb') as image_file:
            files = {"image": image_file}
            response = requests.post(BACKEND_URL, files=files, data=TEST_PARAMS)
        
        print(f"[✅] Status Code: {response.status_code}")
        
        if response.ok:
            print(f"[📦] Response JSON:\n{response.json()}")
        else:
            print(f"[❌] Error:\n{response.text}")
    
    except requests.exceptions.ConnectionError:
        print(f"[❌] Could not connect to backend at {BACKEND_URL}")
    except Exception as e:
        print(f"[💥] Unexpected error: {e}")

if __name__ == "__main__":
    test_generate_image()
