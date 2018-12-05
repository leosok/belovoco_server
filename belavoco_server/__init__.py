from flask import Flask, redirect, url_for, render_template, request
from flask_bootstrap import Bootstrap
import os
#Blueprints
from belavoco_server.app_uploader.controllers import app_uploader
from belavoco_server.api.controllers import api


from base_config import APP_ROOT, UPLOAD_FOLDER



app = Flask(__name__,
            instance_relative_config=True,
            template_folder='templates') 
            
#loading instance config (sensitive!)
app.config.from_pyfile('config.py')


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#Maximum Size:
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
app.config['APP_ROOT'] = APP_ROOT
app.config['SEND_PUSH'] = True
app.config['ADMIN_EMAILS'] = ["maxgraeber@gmail.com", "l.sokolov@mailbox.org"]

app.config['SILENT_PUSH_MAIL'] = 'silent@push'

bootstrap = Bootstrap(app)

app.register_blueprint(api, url_prefix='/api')
#TODO: Remove "File-Panel"
app.register_blueprint(app_uploader, url_prefix='/file-panel')



# Activating Flask-Admin:
# This is the simple Admin Version!

# Create admin
from admin_interface import *


# End of Flask-Admin
@app.route("/file-panel", methods=['GET'])
def main():
    return redirect(url_for('app_uploader.index'))

@app.route("/", methods=['GET'])
def new_upload():
    return render_template('main_upload.html', upload_url='/file-panel/upload')


@app.route("/upload", methods=['GET, POST'])
def go_up():
    return redirect(url_for('app_uploader.upload'))


