import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from trading_bot.utils.utils import Utils

if Utils.is_test():
    uri = 'sqlite:///:memory:'
else:
    uri = r'sqlite:///{}/database/trading_bot.sqlite'.format(os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..')))

app = Flask(__name__, template_folder='../../templates/')
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app, session_options={'expire_on_commit': False})
