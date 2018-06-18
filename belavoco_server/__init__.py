from flask import Flask
from flask_bootstrap import Bootstrap
import os
from belavoco_server.app_uploader.controllers import app_uploader
from belavoco_server.api.controllers import api


UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..',
    'data')

app = Flask(__name__,
            instance_relative_config=True,
            template_folder='templates') 


app.config['SECRET_KEY'] = 'hard to guess string'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#Maximum Size:
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

bootstrap = Bootstrap(app)

app.register_blueprint(app_uploader, url_prefix='')
app.register_blueprint(api, url_prefix='/api')