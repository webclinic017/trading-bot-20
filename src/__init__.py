import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

if len(sys.argv) > 0 and 'test' in sys.argv[0]:
    uri = 'sqlite:///:memory:'
else:
    uri = r'sqlite:///{}/database/tradingbot.sqlite'.format(os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..')))

app = Flask(__name__, template_folder='../templates/')
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
