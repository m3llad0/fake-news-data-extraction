from app.services.flask_server import FlaskServer
from flask_cors import CORS
from app.config import Config
from app.routes import routes

server = FlaskServer("app", Config)

server.add_blueprint(routes, url_prefix='/')

app = server.create_app()

CORS(app)
