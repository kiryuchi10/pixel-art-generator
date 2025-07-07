from tensorflow.keras.models import load_model

def load_text_to_pixel_model():
    return load_model("models/ModelPixelArt.keras")
