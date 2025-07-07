from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

# Load the image-to-pixel art model
def load_image_to_pixel_model():
    return load_model("models/MB5.keras")

# Example helper to process and predict
def preprocess_image(image_path, target_size=(64, 64)):
    image = Image.open(image_path).convert('RGB')
    image = image.resize(target_size)
    return np.expand_dims(np.array(image) / 255.0, axis=0)

def generate_pixel_art(model, image_path):
    processed_image = preprocess_image(image_path)
    output = model.predict(processed_image)
    output_image = (output[0] * 255).astype(np.uint8)
    return Image.fromarray(output_image)
