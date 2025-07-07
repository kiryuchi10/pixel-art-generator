# backend/app/routes/api.py
from flask import Blueprint, request, jsonify
from services.generate import generate_from_text, generate_from_image
from services.exporter import export_image
from services.history import fetch_history

api = Blueprint('api', __name__)

@api.route('/generate/text', methods=['POST'])
def generate_text():
    data = request.get_json()
    try:
        job_id = generate_from_text(data)
        return jsonify({'job_id': job_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/generate/image', methods=['POST'])
def generate_image():
    try:
        image_file = request.files['image']
        params = request.form.to_dict()
        job_id = generate_from_image(image_file, params)
        return jsonify({'job_id': job_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/export', methods=['POST'])
def export():
    data = request.get_json()
    try:
        blob = export_image(data['image_url'], data['format'])
        return blob, 200, {'Content-Type': 'application/octet-stream'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/history', methods=['GET'])
def history():
    try:
        history_data = fetch_history()
        return jsonify({'generations': history_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
