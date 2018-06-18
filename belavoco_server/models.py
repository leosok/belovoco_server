# models.py
import peewee

import datetime
 
database = peewee.SqliteDatabase("uploads.db")
BASE_FILES_URL = 'localhost:5000'
 

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
    #information_text  = TextField()
    

    @staticmethod
    def get_by_hash(hash):
        return Audiofile.select().where(Audiofile.hash == hash).get()

    class Meta:
        database = database
 
 
if __name__ == "__main__":
    try:
        Audiofile.create_table()
    except peewee.OperationalError:
        print "Audiofile table already exists!"