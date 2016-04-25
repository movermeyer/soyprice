from flask import Flask
from config import config


app = Flask(__name__)
app.config.update(config)
app.secret_key = app.config['SECRET_KEY']
