from flask import Flask, redirect, url_for, render_template, request
from flask_bootstrap import Bootstrap
import os
#Blueprints
from belavoco_server.app_uploader.controllers import app_uploader
from belavoco_server.api.controllers import api


from base_config import APP_ROOT, UPLOAD_FOLDER


import flask_admin as admin

from flask_admin.contrib.fileadmin import FileAdmin
from belavoco_server.models import UserAdmin, User, AudioAdmin, Audiofile


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


# Activating Flask-Admin:

   


import user_managment

# Create admin
admin = admin.Admin(app, 'Example: Auth', index_view=user_managment.MyAdminIndexView(), base_template='my_master.html')

# Add view
#admin.add_view(MyModelView(User, db.session))
#admin = admin.Admin(app, name='BelaVoco Admin')
admin.add_view(UserAdmin(User))   
admin.add_view(AudioAdmin(Audiofile)) 


from os import path as op
#admin.add_view(FileAdmin(app.config['UPLOAD_FOLDER'], name='Files'))   

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


