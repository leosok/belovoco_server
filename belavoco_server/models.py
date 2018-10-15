# models.py
import peewee
import datetime

import os
from base_config import APP_ROOT

#import flask_admin as admin
#from flask_admin.contrib.peewee import ModelView
#from flask_security import current_user, login_required, RoleMixin, Security, \
#    PeeweeUserDatastore, UserMixin, utils
#from flask_login import login_manager

import sys
#### LOGIN
""" from flask_login import AnonymousUserMixin
class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.username = 'Guest'
 """
 ##### END OF LOGIN


DB_FILE_UPLOADS = os.path.join(APP_ROOT, "uploads.db")
DB_FILE_USERS = os.path.join(APP_ROOT, "users.db")

database_uploads = peewee.SqliteDatabase(DB_FILE_UPLOADS)
database_users   = peewee.SqliteDatabase(DB_FILE_USERS)


#print DB_FILE_UPLOADS

#BASE_FILES_URL = 'localhost:5000'


class Audiofile(peewee.Model):
    """
    ORM model of album table
    """
    author = peewee.CharField()
    file_name =  peewee.CharField()
    reader = peewee.CharField()
    title  = peewee.CharField()
    upload_time = peewee.DateTimeField(default=datetime.datetime.now)
    length = peewee.CharField()
    times_played = peewee.IntegerField(default=0)
    times_liked = peewee.IntegerField(default=0)
    file_size =  peewee.IntegerField()
    file_url  =  peewee.CharField(default='')
    hash = peewee.CharField(default=0, unique=True)
    text_info  = peewee.TextField(default = '')
    text_lang = peewee.CharField(default='de')
    text_type = peewee.IntegerField(default=0)
    
    
  
    @staticmethod
    def get_by_hash(hash):
        return Audiofile.select().where(Audiofile.hash == hash).get()
    
    def get_text_type(self):
        ttypes ["unknown","Prosa","Lyrik"]
        return ttypes[self.text_type]
 
    class Meta:
        database = database_uploads




class User(peewee.Model):
    """
    ORM model Users table - right now only with little fields
    """
    
    user_email = peewee.CharField(primary_key=True)
    user_name = peewee.CharField()
    hash = peewee.CharField()
    time_of_registration = peewee.DateTimeField(default=datetime.datetime.now)
    player_id = peewee.CharField(default="0")

    class Meta:
        database = database_users
 
# Classes for Flask-Admin 
import flask_admin as admin
from flask_admin.contrib.peewee import ModelView


class UserAdmin(ModelView):
    column_exclude_list = ['']
    column_searchable_list = ('user_email','user_name')
    #column_filters = ('user_email',)

    '''
    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        else:
            return True
    '''

class AudioAdmin(ModelView):
    column_exclude_list = [''] 
    '''
    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        else:
            return True
    '''

if __name__ == "__main__":

    import logging
    logger = logging.getLogger('peewee')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    try:
        Audiofile.create_table()
        print "Created Audiofil table"
    except peewee.OperationalError:
        print "Audiofile table already exists!"
    try:
        User.create_table()
        print "Created User table"
    except peewee.OperationalError:
        print "User table already exists!"