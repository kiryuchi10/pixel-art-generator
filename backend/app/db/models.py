from . import db

class Generation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_text = db.Column(db.Text)
    output_image_url = db.Column(db.String(255))
    style_type = db.Column(db.String(50))
    resolution = db.Column(db.String(20))
