# models.py
import peewee
from peewee import *

from playhouse.shortcuts import model_to_dict

import datetime

import os
from base_config import APP_ROOT
import json

#import flask_admin as admin
from flask_admin.contrib.peewee import ModelView
from flask_admin.model.template import EndpointLinkRowAction, LinkRowAction
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
 # 

DATABASE = os.path.join( APP_ROOT, 'bv_v2_database.db')

database = peewee.SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta:
        database = database



class User(BaseModel):
    """
    ORM model Users table - right now only with little fields
    """
    #TODO: added Unique Constraint - rebuild Database (19.10.18, Leo)
    user_email = CharField(unique=True)
    user_name = CharField()
    hash = CharField()
    time_of_registration = DateTimeField(default=datetime.datetime.now)
    player_id = CharField(default="0")

    class Meta:
        table_name = 'users'

    #This will lead to the Email showing in Flask-Admin instead of ID
    def __unicode__(self):
        return self.user_email

    def get_all_audios(self):
        """ Returns all not-blocked audiofiles for user """        
            
        blocked_audios = Audiofile.select().join(Audio_not_allowed).where(Audio_not_allowed.user == self)
        #get all audios which are not in the blocked_audios
        audios_not_blocked = Audiofile.select().where((Audiofile.id.not_in(blocked_audios)) and (Audiofile.is_active == True) )
        return audios_not_blocked

    def get_all_audios_as_json(self):
            
        all_records = []
        for a in self.get_all_audios():             
            a_dict = model_to_dict(a) 
            #add a value "liked", audio is liked by self(user)
            a_dict['liked'] = a.is_liked(self)
            #a_dict['times_liked'] = a.count_likes()
            #print a_dict        
            all_records.append(a_dict)        

        #print json.dumps(all_records, indent=4, sort_keys=True, default=str)

        return json.dumps(all_records, indent=4, sort_keys=True, default=str)


    def like(self,audiofile):
        try:
            Like.create(
                    user=self,
                    audiofile=audiofile )
        except IntegrityError:
        #This like did exist - so we UNLIKE
            like_query = Like.select().where(Like.user==self,
                        Like.audiofile==audiofile)            
            like_query.get().delete_instance()

        Audiofile.update(times_liked = audiofile.count_likes()).\
                        where(Audiofile.hash == audiofile.hash).\
                        execute()

    class Meta:
        table_name = 'users'



class UserAdmin(ModelView):

    column_exclude_list = ['']
    column_searchable_list = ('user_email','user_name')
    #column_filters = ('user_email', 'user_name')
    #column_filters = ('user_user_email',)

    '''
    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        else:
            return True
    '''



class Audiofile(BaseModel):
    """
    ORM model of album table
    """
    author = CharField()
    file_name =  CharField()
    reader = CharField()
    title  = CharField()
    upload_time = DateTimeField(default=datetime.datetime.now)
    length = CharField()
    times_played = IntegerField(default=0)
    times_liked = IntegerField(default=0)
    file_size =  IntegerField()
    file_url  =  CharField(default='')
    hash = CharField(default=0, unique=True)
    text_info  = TextField(default = '')
    text_lang = CharField(default='de')
    text_type = IntegerField(default=0)

    creator = ForeignKeyField(User, backref='users', default=1)
    is_active = BooleanField(default=True)

    #This will lead to the Title showing in Flask-Admin instead of ID
    def __unicode__(self):
        return self.title
    
    class Meta:
        table_name = 'audiofiles'

    def create_comment(self,user,content):
        Comment.create( user = user,
                        audiofile = self,
                        content = content,
                        )

    def get_comments(self):
        return Comment.select().where(Comment.audiofile == self).order_by(Comment.pub_date.desc())


    def get_comments_json(self):
        #Returns a json ready for sending to Cilent
        comments = []
        for ac in Audiofile.get_by_hash(self.hash).get_comments():
            comment = {}

            comment['user'] = model_to_dict(ac.user)
            comment['pub_date'] = ac.pub_date
            comment['content'] = ac.content
            comment['id'] = ac.id
            comments.append(comment)

        return json.dumps(comments, indent=4, sort_keys=True, default=str)


    def count_likes(self):
       
        return Like.select().where(Like.audiofile == self ).count()

    def is_liked(self,user):
         return Like.select().where(Like.audiofile == self , Like.user == user).count()
    
    def add_played(self,user):
        Play.create(audiofile = self, user = user)
        Audiofile.update(times_played = self.count_plays()).\
                        where(Audiofile.hash == self.hash).\
                        execute()


    def count_plays(self):
        return Play.select().where(Play.audiofile == self ).count()
        
        #return Like.select(fn.COUNT()).where(Like.audiofile == self ).count()

    @staticmethod
    def get_by_hash(hash):
        return Audiofile.select().where(Audiofile.hash == hash).get()
    
    def get_text_type(self):
        ttypes ["unknown","Prosa","Lyrik"]
        return ttypes[self.text_type]

    class Meta:
        table_name = 'audiofiles'


class AudioAdmin(ModelView):
    column_exclude_list = [''] 
    column_searchable_list = ('title',)
    column_editable_list = ('file_name','file_url','is_active' )
    #column_filters = ('user_email', 'user_name')
    #column_filters = ('user_user_email',)

    button_js = ''' '''

    column_extra_row_actions = [
        LinkRowAction('glyphicon glyphicon-new-window icon-new-window', '{row_id}'),
    ]



class Audio_allowed(BaseModel):   
        
    audiofile = ForeignKeyField(Audiofile, backref='audiofile')
    user = ForeignKeyField(User, backref='user')

    class Meta:
        indexes = (
            # Specify a unique multi-column index on from/to-user.
            (('audiofile', 'user'), True),
        )




class Audio_not_allowed(BaseModel):
       
    audiofile = ForeignKeyField(Audiofile, backref='audiofile')
    user = ForeignKeyField(User, backref='user')

    class Meta:
        indexes = (
            # Specify a unique multi-column index on from/to-user.
            (('audiofile', 'user'), True),
        )

class Standard_Admin(ModelView):
    column_exclude_list = [''] 
    column_editable_list = ('user', )



# this model contains two foreign keys to user -- it essentially allows us to
# model a "many-to-many" relationship between users.  by querying and joining
# on different columns we can expose who a user is "related to" and who is
# "related to" a given user
class Like(BaseModel):
   
    audiofile = ForeignKeyField(Audiofile, backref='audiofile')
    user = ForeignKeyField(User, backref='user')

    class Meta:
        indexes = (
            # Specify a unique multi-column index on from/to-user.
            (('audiofile', 'user'), True),
        )
    
        table_name = 'likes'


class Play(BaseModel):
   
    audiofile = ForeignKeyField(Audiofile, backref='audiofile')
    user = ForeignKeyField(User, backref='user')
    play_time = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        indexes = (
            (('audiofile', 'user'), False),
        )
    
        table_name = 'plays'

    

#TODO: Comments
class Comment(BaseModel):
    audiofile = ForeignKeyField(Audiofile, backref='comments')
    user = ForeignKeyField(User, backref='comments')
    content = TextField()
    pub_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'comments'

    @staticmethod
    def delete_comment(del_id, current_user):
        try:
            comment_delete_query = Comment.select().where((Comment.id == del_id) & (Comment.user == current_user ))            
            comment_to_delete = comment_delete_query.get()   
            comment_to_delete.delete_instance()
            print "Here delete_comment. Deleting CommentID {} Content: {}".format(comment_to_delete.id,comment_to_delete.content)
        except IntegrityError:
            print "Comment (ID){} could not be deleted. Wrong user? Does not exist? {}".format(del_id)
        
      
        return True

# simple utility function to create tables
def create_tables():
    with database:
        database.create_tables([User, Like, Play,  Audiofile, Comment, Audio_allowed, Audio_not_allowed])

def create_admin():
    User.create(user_name = 'Admin', user_email = 'info@belavo.co', hash = '99996666613')



if __name__ == "__main__":


    #import logging
    #logger = logging.getLogger('peewee')
    #logger.setLevel(logging.DEBUG)
    #logger.addHandler(logging.StreamHandler())
    print "Trying to create databases in: " + DATABASE
    create_tables()
    create_admin()
    print "Database created!"