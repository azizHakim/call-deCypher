import sys
from flask import Flask
from flasgger import Swagger
from flask import Flask, send_from_directory
from flask_cors import CORS
#import latest sqlite


app = Flask(__name__)
CORS(app)
app.config.from_object('config.LocalConfig')

from app import route