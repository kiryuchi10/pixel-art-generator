import os
import numpy as np
from keras.models import load_model
from PIL import Image

# === CONFIG ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_TEXT_PATH = os.path.join(BASE_DIR, "app", "models", "ModelPixelArt.keras")
MODEL_IMAGE_PATH = os.path.join(BASE_DIR, "app", "models", "MB5.keras")
TEST_IMAGE_PATH = os.path.join(BASE_DIR, "test_assets", "KakaoTalk_20250708_231845951.jpg")

def load_image_for_model(path, size=(32, 32)):
    try:
        img = Image.open(path).convert("RGB").resize(size)
        arr = np.array(img) / 255.0
        arr = np.expand_dims(arr, axis=0)  # (1, H, W, 3)
        return arr
    except Exception as e:
        print(f"[❌] Error loading image: {e}")
        return None

def test_model(model_path, input_shape):
    try:
        print(f"[📦] Loading model: {model_path}")
        model = load_model(model_path, compile=False)
        model.summary()

        dummy_input = np.random.rand(*input_shape).astype(np.float32)
        output = model.predict(dummy_input)
        print(f"[✅] Inference successful. Output shape: {output.shape}")

    except OSError as e:
        print(f"[❌] Model loading failed (possible corruption): {e}")
    except Exception as e:
        print(f"[💥] Model test failed: {e}")

def test_model_with_image(model_path, image_path):
    img_input = load_image_for_model(image_path)
    if img_input is None:
        return

    try:
        model = load_model(model_path, compile=False)
        output = model.predict(img_input)
        print(f"[✅] Prediction succeeded. Output shape: {output.shape}")
    except Exception as e:
        print(f"[❌] Prediction error: {e}")

if __name__ == "__main__":
    print("== TEXT MODEL ==")
    test_model(MODEL_TEXT_PATH, input_shape=(1, 32, 32, 3))
    test_model_with_image(MODEL_TEXT_PATH, TEST_IMAGE_PATH)

    print("\n== IMAGE MODEL ==")
    test_model(MODEL_IMAGE_PATH, input_shape=(1, 32, 32, 3))
    test_model_with_image(MODEL_IMAGE_PATH, TEST_IMAGE_PATH)
