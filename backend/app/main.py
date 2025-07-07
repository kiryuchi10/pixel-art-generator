import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent dir to path first

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from db.database import db, init_db
from config import Config
from routes import main as main_routes  # if routes/__init__.py exists

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Initialize DB
init_db(app)
CORS(app)

# Register blueprints
app.register_blueprint(main_routes)

if __name__ == '__main__':
    app.run(debug=True)
