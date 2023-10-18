from flask import Flask
from config import Config
from .site.routes import site
from .auth.routes import auth
from .api.routes import api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db as root_db, login_manager, ma
from flask_cors import CORS
from helpers import JSONEncoder

app = Flask(__name__)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

app.config.from_object(Config)
app.json_encoder = JSONEncoder
root_db.init_app(app)
migrate = Migrate(app, root_db)
ma.init_app(app)
login_manager.init_app(app)