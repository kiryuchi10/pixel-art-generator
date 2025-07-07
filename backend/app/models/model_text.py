from tensorflow.keras.models import load_model

def load_text_to_pixel_model():
    try:
        return load_model(
            "C:/Users/user/Documents/GitHub/pixel-art-generator/pixel-art-generator/backend/app/models/ModelPixelArt.keras",
            compile=False
        )
    except Exception as e:
        print("Failed to load text-to-pixel model:", e)
        raise
