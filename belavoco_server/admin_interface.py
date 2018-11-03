# -*- coding: utf-8 -*-
# Here we create the admin-interface for BV


import flask_admin as admin
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import Admin, AdminIndexView, expose
from belavoco_server.models import UserAdmin, User, AudioAdmin, Audiofile, Audio_not_allowed, Like, Play
from flask_admin.contrib.peewee import ModelView
from flask_admin.model.template import EndpointLinkRowAction, LinkRowAction



class HomeView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render('admin/home.html', users=User)

class Standard_Admin(ModelView):
    column_exclude_list = [''] 
    column_editable_list = ('user', )

from belavoco_server import app

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

admin.add_view(Standard_Admin(Audio_not_allowed))
admin.add_view(Standard_Admin(Like))
admin.add_view(Standard_Admin(Play))

from os import path as op
admin.add_view(FileAdmin(app.config['UPLOAD_FOLDER'], name='Files'))   

