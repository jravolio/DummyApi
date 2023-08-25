from flask import Flask
from .db import Database

def create_app():
    app = Flask(__name__)
    
    # Load configuration settings from a config file (e.g., config.py)
    app.config.from_pyfile('config.py')

    # Initialize the database connection
    db = Database()
    db.init_app(app)

    # Register the API blueprint
    from .routes import api_bp
    app.register_blueprint(api_bp)

    return app
