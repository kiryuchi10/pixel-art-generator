from models.model_text import load_text_to_pixel_model
from models.model_image import load_image_to_pixel_model
import os

text_model = load_text_to_pixel_model()
image_model = load_image_to_pixel_model()

def generate_from_text(text, style, resolution):
    img = text_model.predict([text])
    output_path = f"static/generated/{text[:10]}_{resolution}.png"
    # Save logic here
    return output_path
