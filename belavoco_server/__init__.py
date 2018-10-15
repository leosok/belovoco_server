from flask import Flask, redirect, url_for, render_template, request
from flask_bootstrap import Bootstrap
import os
#Blueprints
from belavoco_server.app_uploader.controllers import app_uploader
from belavoco_server.api.controllers import api


from base_config import APP_ROOT, UPLOAD_FOLDER


import flask_admin as admin

from flask_admin.contrib.fileadmin import FileAdmin

from flask_admin import Admin, AdminIndexView, expose

from belavoco_server.models import UserAdmin, User, AudioAdmin, Audiofile


app = Flask(__name__,
            instance_relative_config=True,
            template_folder='templates') 
            
#loading instance config (sensitive!)
app.config.from_pyfile('config.py')


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#Maximum Size:
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['APP_ROOT'] = APP_ROOT

bootstrap = Bootstrap(app)

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(app_uploader, url_prefix='/file-panel')



# Activating Flask-Admin:
# This is the simple Admin Version!

# Create admin


class HomeView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render('admin/home.html', users=User)

admin = Admin(app, "BV Admin", 
            index_view=HomeView(name='Home1', menu_icon_type='glyph', menu_icon_value='glyphicon-home', url=app.config['ADMIN_URL']),       
            template_mode='bootstrap3',  url=app.config['ADMIN_URL'],
            )


#admin = admin.Admin(app, 'BV Admin', url=app.config['ADMIN_URL'])

# Add view
#admin.add_view(MyModelView(User, db.session))
#admin = admin.Admin(app, name='BelaVoco Admin')
admin.add_view(UserAdmin(User))   
admin.add_view(AudioAdmin(Audiofile)) 
from os import path as op
admin.add_view(FileAdmin(app.config['UPLOAD_FOLDER'], name='Files'))   



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


