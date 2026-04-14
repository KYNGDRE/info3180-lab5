from flask import Flask
from .config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
csrf = CSRFProtect(app)
app.config.from_object(Config)

db = SQLAlchemy(app) 
migrate = Migrate(app, db)

from app import views
from app import models  