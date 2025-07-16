from app.services.flask_server import FlaskServer
from flask_cors import CORS
from app.config import Config
from app.routes import routes
import os
import certifi
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

server = FlaskServer("app", Config)

server.add_blueprint(routes, url_prefix='/')

app = server.create_app()

CORS(app)
