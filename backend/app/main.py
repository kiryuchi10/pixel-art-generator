from flask import Flask
from flask_cors import CORS
from db.database import db
from routes import main
from config import Config
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
CORS(app)

app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
