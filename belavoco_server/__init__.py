from flask import Flask, redirect, url_for, render_template
from flask_bootstrap import Bootstrap
import os
from belavoco_server.app_uploader.controllers import app_uploader
from belavoco_server.api.controllers import api

from base_config import APP_ROOT, UPLOAD_FOLDER

app = Flask(__name__,
            instance_relative_config=True,
            template_folder='templates') 


app.config['SECRET_KEY'] = 'hard to guess string'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#Maximum Size:
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['APP_ROOT'] = APP_ROOT

bootstrap = Bootstrap(app)

app.register_blueprint(app_uploader, url_prefix='/file-panel')
app.register_blueprint(api, url_prefix='/api')

@app.route("/", methods=['GET'])
def main():
    return redirect(url_for('app_uploader.index'))

@app.route("/fp", methods=['GET'])
def new_upload():
    return render_template('main_upload.html')