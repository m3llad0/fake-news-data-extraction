from app import app
from flask_cors import CORS

CORS(app)

@app.route('/')
def index():
    return "Hello, World!"