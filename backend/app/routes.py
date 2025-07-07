from flask import Blueprint, request, jsonify
from services.generate import generate_from_text
from celery_worker import process_text_generation

main = Blueprint('main', __name__)

@main.route('/api/generate/text', methods=['POST'])
def generate_text():
    data = request.json
    job = process_text_generation.delay(
        data['text'], data['style'], data['resolution']
    )
    return jsonify({"jobId": job.id})
