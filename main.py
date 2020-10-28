import os
import sys
import configparser
from flask import Flask

config_path = os.path.join('config', 'config.ini')

if not os.path.isfile(config_path):
    print(f'No file: {config_path}')
    sys.exit(1)

config = configparser.ConfigParser()
config.read(config_path)

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'
