from flask import Flask
from app.routes import api_bp
from app.db import Database

app = Flask(__name__)
db = Database()
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(threaded=True, host="0.0.0.0", port=5003)
