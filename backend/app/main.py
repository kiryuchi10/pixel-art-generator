from flask import Flask
from routes import main  # ✅ This must match the filename (routes.py)

def create_app():
    app = Flask(__name__)

    # DB setup here if needed
    app.config.from_object("config.Config")

    from db.database import db
    db.init_app(app)

    # Register blueprint
    app.register_blueprint(main)  # ✅ Register routes from routes.py

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
