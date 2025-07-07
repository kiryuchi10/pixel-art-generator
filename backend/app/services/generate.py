# Before
# from models.model_text import load_text_to_pixel_model
# text_model = load_text_to_pixel_model()

# After — define this as a cached lazy loader
from models.model_text import load_text_to_pixel_model

_text_model = None  # lazy cache

def generate_from_text(data):
    global _text_model
    if _text_model is None:
        _text_model = load_text_to_pixel_model()

    prompt = data['text']
    # your generation logic using _text_model
    return {
        "job_id": "job123",
        "status": "started"
    }
    
def generate_pixel_art_task(*args, **kwargs):
    print("generate_pixel_art_task called - placeholder only.")

def generate_from_image_task(*args, **kwargs):
    print("generate_from_image_task called - placeholder only.")
