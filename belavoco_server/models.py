# models.py
import peewee
import datetime

import os
from base_config import APP_ROOT

DB_FILE = os.path.join(APP_ROOT, "uploads.db")
database = peewee.SqliteDatabase(DB_FILE)

print DB_FILE

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
    hash = peewee.CharField(default=0)
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
        database = database
 
 
if __name__ == "__main__":
    try:
        Audiofile.create_table()
    except peewee.OperationalError:
        print "Audiofile table already exists!"