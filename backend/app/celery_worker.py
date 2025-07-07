from celery import Celery
from services.generate import generate_from_text
from main import app

celery = Celery(__name__)
celery.config_from_object('config.Config')

@celery.task()
def process_text_generation(text, style, resolution):
    with app.app_context():
        result = generate_from_text(text, style, resolution)
        return result
