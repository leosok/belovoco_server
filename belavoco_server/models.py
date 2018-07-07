# models.py
import peewee
import datetime

import os
from base_config import APP_ROOT

import sys

DB_FILE_UPLOADS = os.path.join(APP_ROOT, "uploads.db")
DB_FILE_USERS = os.path.join(APP_ROOT, "users.db")

database_uploads = peewee.SqliteDatabase(DB_FILE_UPLOADS)
database_users   = peewee.SqliteDatabase(DB_FILE_USERS)

print DB_FILE_UPLOADS

#BASE_FILES_URL = 'localhost:5000'
 

class Audiofile(peewee.Model):
    """
    ORM model of album table
    """
    file_name =  peewee.CharField()
    reader = peewee.CharField()
    author = peewee.CharField()
    title  = peewee.CharField()
    upload_time = peewee.DateTimeField(default=datetime.datetime.now)
    length = peewee.CharField()
    times_played = peewee.IntegerField(default=0)
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
    username =  peewee.CharField()
    token = peewee.CharField(unique=True)
    time_of_registration = peewee.DateTimeField(default=datetime.datetime.now)


    class Meta:
        database = database_users
 


 
if __name__ == "__main__":
    try:
        Audiofile.create_table()
        print "created Audiofil table"
    except peewee.OperationalError:
        print "Audiofile table already exists!"
    try:
        User.create_table()
        print "Created User table"
    except peewee.OperationalError:
        print "User table already exists!"