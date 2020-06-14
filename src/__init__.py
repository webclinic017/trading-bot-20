import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../templates/')
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///{}/database/tradingbot.sqlite'.format(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
