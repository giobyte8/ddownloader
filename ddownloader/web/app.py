from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
import ddownloader.web.api

CORS(app)
