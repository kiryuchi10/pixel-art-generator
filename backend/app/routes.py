from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid

from db.database import db
from db.models import Generation
from services.generate import generate_pixel_art_task, generate_from_image_task

main = Blueprint("main", __name__)

UPLOAD_FOLDER = "static/uploads"


@main.route("/generate/text", methods=["POST"])
def generate_from_text():
    try:
        data = request.get_json()

        job_id = str(uuid.uuid4())
        generation = Generation(
            id=job_id,
            input_text=data["text"],
            style_type=data["style"],
            resolution=data["resolution"],
            color_palette=data["color_palette"],
            batch_count=data.get("batch_count", 1),
            status="pending",
            created_at=datetime.utcnow()
        )

        db.session.add(generation)
        db.session.commit()

        generate_pixel_art_task.apply_async(
            args=[
                data["text"],
                data["style"],
                data["resolution"],
                data["color_palette"],
                data.get("batch_count", 1),
                job_id
            ],
            task_id=job_id
        )

        return jsonify({"job_id": job_id, "status": "pending", "message": "Text generation started"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route("/generate/image", methods=["POST"])
def generate_from_image():
    try:
        image = request.files.get("image")
        style = request.form.get("style", "8bit")
        resolution = request.form.get("resolution", "32x32")
        color_palette = request.form.get("color_palette", "classic")
        batch_count = int(request.form.get("batch_count", 1))

        if not image:
            return jsonify({"error": "Image is required"}), 400

        job_id = str(uuid.uuid4())
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filename = secure_filename(f"{job_id}_{image.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        image.save(filepath)

        generation = Generation(
            id=job_id,
            input_image_url=filepath,
            style_type=style,
            resolution=resolution,
            color_palette=color_palette,
            batch_count=batch_count,
            status="pending",
            created_at=datetime.utcnow()
        )

        db.session.add(generation)
        db.session.commit()

        generate_from_image_task.apply_async(
            args=[filepath, style, resolution, color_palette, batch_count, job_id],
            task_id=job_id
        )

        return jsonify({"job_id": job_id, "status": "pending", "message": "Image generation started"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route("/generation/<job_id>/status", methods=["GET"])
def get_generation_status(job_id):
    try:
        generation = Generation.query.filter_by(id=job_id).first()
        if not generation:
            return jsonify({"error": "Job not found"}), 404

        return jsonify({
            "job_id": generation.id,
            "status": generation.status,
            "progress": generation.progress or 0,
            "result_url": generation.output_image_url,
            "error": generation.error_message,
            "created_at": generation.created_at,
            "completed_at": generation.completed_at
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
