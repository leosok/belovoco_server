from flask import Flask
from flask_bootstrap import Bootstrap

from belavoco_server.app_uploader.controllers import app_uploader
from belavoco_server.api.controllers import api


app = Flask(__name__,
            instance_relative_config=True,
            template_folder='templates') 


app.config['SECRET_KEY'] = 'hard to guess string'
app.config['UPLOAD_FOLDER'] = 'data'
#Maximum Size:
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

bootstrap = Bootstrap(app)

app.register_blueprint(app_uploader, url_prefix='')
app.register_blueprint(api, url_prefix='/api')