# -*- coding: utf-8 -*-
# Here we create the admin-interface for BV


import flask_admin as admin
from flask_admin.actions import action
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import Admin, AdminIndexView, expose
from belavoco_server.models import  User, Comment
from belavoco_server.models import Audiofile, Audio_not_allowed, Like, Play
from flask_admin.contrib.peewee import ModelView
from flask_admin.model.template import EndpointLinkRowAction, LinkRowAction

from flask import request, url_for
from flask import current_app
from belavoco_server import app



from datetime import date
from flask_admin.model import typefmt

def date_format(view, value):
    return value.strftime('%d.%m.%y - %H:%M')

DATE_FORMATTER = dict(typefmt.BASE_FORMATTERS)
DATE_FORMATTER.update({
        type(None): typefmt.null_formatter, 
        date: date_format
    })



class HomeView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render('admin/home.html', users=User)

class Standard_Admin(ModelView):
    column_exclude_list = [''] 
    column_editable_list = ('user', )
    column_default_sort = ('id', True)


class AudioAdmin(ModelView):
    column_exclude_list = [''] 
    column_searchable_list = ('title',)
    column_editable_list = ('file_name','file_url','is_active','creator' )

    column_default_sort = ('id', True)


    button_js = ''' '''

    """ column_extra_row_actions = [
        LinkRowAction('glyphicon glyphicon-new-window icon-new-window', '{row_id}'),
    ]
    """


class NewUserView(ModelView):
    
   
    list_template = 'admin/model/custom_list.html'
    page_size = 10

    #open-modal is inline-JS in custom_list.html
    column_extra_row_actions = [
        LinkRowAction('glyphicon glyphicon-new-window icon-new-window', 'javascript:openModal({row_id})'),
    ]

    column_exclude_list = ['hash']
    column_filters = ('user_email', 'user_name', 'app_version')
    column_editable_list = ('user_email','user_name', )
    column_default_sort = ('id', True)
    
    column_type_formatters = DATE_FORMATTER

    # omitting the third argument suppresses the confirmation alert
    @action('change_cost', 'Change Cost')
    def action_change_cost(self, ids):
        url = get_redirect_target() or self.get_url('.index_view')
        return redirect(url, code=307)

    @expose('/modal/<id>')
    def index(self,id):
        #return "Gut, so sei es, {}".format(User.select().where(User.id == id).get().user_name)
        this_user = User.select().where(User.id == id).get()
        #return Audiofile.select().where(Audiofile.creator == this_user).first().title
        
        audiofiles =  Audiofile.select().where(Audiofile.creator == this_user)
        try:
            plays = Play.select(Play.audiofile).where(Play.user == this_user ).distinct()
            play_infos = []
            for play in plays:
                play_info = {}
                play_info['name'] = play.audiofile.title
                play_info['count'] = Play.select().where((Play.user == this_user) & (Play.audiofile == play.audiofile)).count()
                play_info['is_liked'] = Like.select().where((Like.user == this_user) & (Like.audiofile == play.audiofile)).count()
                play_infos.append(play_info)
            #print plays.audiofile.title
        except:
            plays = None
            print "Some Error when trying to show Plays by user"
            pass
        
        #print play_infos
        return self.render('admin/user_modal.html', user= this_user , audiofiles=audiofiles, play_infos = play_infos)



from belavoco_server import app

admin = Admin(app, "BV Admin", 
            index_view=HomeView(name='Home1', menu_icon_type='glyph', menu_icon_value='glyphicon-home', url=app.config['ADMIN_URL']),       
            template_mode='bootstrap3',  url=app.config['ADMIN_URL'],
            )


#admin = admin.Admin(app, 'BV Admin', url=app.config['ADMIN_URL'])

# Add view
#admin.add_view(MyModelView(User, db.session))
#admin = admin.Admin(app, name='BelaVoco Admin')
#admin.add_view(UserAdmin(User))  
admin.add_view(NewUserView(User,endpoint='user'))

admin.add_view(AudioAdmin(Audiofile)) 

admin.add_view(Standard_Admin(Audio_not_allowed))
admin.add_view(Standard_Admin(Like))
admin.add_view(Standard_Admin(Play))
admin.add_view(Standard_Admin(Comment))


from os import path as op
admin.add_view(FileAdmin(app.config['UPLOAD_FOLDER'], name='Files'))   

