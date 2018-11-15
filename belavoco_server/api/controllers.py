# -*- coding: utf-8 -*-

from flask import Blueprint

# BLUEPRINT #####################
api = Blueprint('api', __name__)
from flask import current_app as app
# BLUEPRINT #####################

from playhouse.shortcuts import model_to_dict


from belavoco_server.models import Audiofile, User, Comment

from flask import jsonify, abort
from flask import send_file, request, Response
from functools import wraps
from flask import abort
#from flask import g

import json
import simplejson
import os, sys
import re
import mimetypes
from werkzeug.security import generate_password_hash



import logging
import hashlib
from peewee import DoesNotExist

from comments import ctrl_comments


def play_seeking(path, the_request):

    range_header = the_request.headers.get('Range', None)
    #print the_request.headers
    if not range_header:
        #print "just sending a file"
        return send_file(path)
    else:
        size = os.path.getsize(path)
        byte1, byte2 = 0, None

        m = re.search('(\d+)-(\d*)', range_header)
        g = m.groups()

        if g[0]: byte1 = int(g[0])
        if g[1]: byte2 = int(g[1])

        length = size - byte1
        if byte2 is not None:
            length = byte2 + 1 - byte1

        data = None
        with open(path, 'rb') as f:
            f.seek(byte1)
            data = f.read(length)

        print "Creating a 206!"

        rv = Response(data,
            206,
            mimetype=mimetypes.guess_type(path)[0],
            direct_passthrough=True)
        rv.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(byte1, byte1 + length - 1, size))
        return rv

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
            if not 'Authorization' in request.headers:
               abort(401)            
            else:            
                request_user_hash = request.headers['Authorization']
                try:
                    #due to iOS implementation of BV the app can send an empty Auth header                    
                    kws['current_user'] = User.select().where(User.hash == request_user_hash).get()
                except:
                    abort(401)

                return f(*args, **kws)            
    return decorated_function


@api.route("/validate_user", methods=['GET'])
def validate_user():

    
    email_to_validate = request.args.get('user_email')
    #print email_to_validate

    #print User.select().where(User.user_email == email_to_validate).get()

    if User.select().where(User.user_email == email_to_validate).count():
        return "Nice!"
    else:
        abort(404, "User not found in Database")
    
    #return "1"

@api.route("/")
def index():
    return "Welcome to BeloVoco JSON-Api"



@api.route('/get/<string:hash_value>/play/<string:filename>', methods=['GET'])
@api.route('/get/<string:hash_value>/play', methods=['GET'])
def play(hash_value,filename='None'): 
        
    this_audio = Audiofile.select().where(Audiofile.hash == hash_value).get()
    data = model_to_dict (this_audio)
    #Add +1 to the Play Counter:
    #TODO: Add a "real" Playcount. Problem: The Trackplayer is not sending a header---
    #this_audio.add_played(current_user)
    """ this_audio.times_played += 1
    this_audio.save()
    """ 
    #Create path & send the file to User
    file_path = os.path.join(app.root_path,'..',this_audio.file_name)
    return play_seeking(file_path,request)


@api.route('/get/<string:hash_value>/play', methods=['PUT'])
@authorize
def inc_playcount(hash_value,current_user=None): 
        
    this_audio = Audiofile.select().where(Audiofile.hash == hash_value).get()
    this_audio.add_played(current_user)
    
    #Create path & send the file to User
    file_path = os.path.join(app.root_path,'..',this_audio.file_name)
    return "ok"


@api.route("/get/<string:hash_value>", methods=['GET'])
@authorize
def get_json(hash_value,action=None,current_user=None):

    #print "Wer ist da? %s" % (current_user)

    if hash_value == 'all':        
        return current_user.get_all_audios_as_json()             

    else: 
        this_audio = Audiofile.select().where(Audiofile.hash == hash_value).get()
        data = model_to_dict (this_audio)
        return json.dumps(data, indent=4, sort_keys=True, default=str)


@api.route('/set/<string:hash_value>/<string:action>', methods=['GET','POST'])
@authorize
def set_like(hash_value,action=None,current_user=None):
    this_audio = Audiofile.select().where(Audiofile.hash == hash_value).get()
    
    #I am getting a Post request with a UserHash
    #TODO: Implement User-Model wich will get the likes instad of the audiofiles! 
    #print request.get_json()
    
    #current_user = authorize_user_from_header(request)

    if (action == 'like') or (action == 'unlike'):
        current_user.like(this_audio)
        #current_user.save()
        print "{}, {}".format(current_user.user_name,this_audio.title)

    #TODO: Like == Unlike :-)
        """   if action == 'unlike':
       
        if this_audio.times_liked > 0:
            this_audio.times_liked -= 1
            this_audio.save() """

    data = model_to_dict (this_audio)
    return json.dumps(data, indent=4, sort_keys=True, default=str)



@api.route("/user", methods=['PUT'])
def user_update():
    
    print request.json
    #authorize_user_from_header(request)

    user_data = request.json.get('user')

    #This is a nicer try-except
    if 'useremail' in user_data:
        user_email = user_data['useremail']
    else: user_email = 'none'

    if 'username' in user_data:
        user_name = user_data['username']
    else: 
        user_name ='Mustermann'
    if 'onesignalid' in user_data:
        user_player_id = user_data['onesignalid']
    else: 
        user_player_id ='0'
    if 'userhash' in user_data:
        user_hash = user_data['userhash']
    else:
        return abort(404)

    user_update = User.update({User.user_email: user_email,
                         User.user_name: user_name, 
                         User.player_id: user_player_id}).\
                        where(User.hash == user_hash ).\
                        execute()
    if user_update:
        print "User was updated: " + User.select().where(User.hash == user_hash ).get().user_email
        return "User updated!"        
    else:
        print "ERROR: Updating a User which does not exist"
        abort(404)


@api.route("/user", methods=['GET'])
def user_stub():
    return "this is user API"

@api.route("/user", methods=['POST'])
def user_create():
  
    user_data = request.json.get('user')
    print user_data

    #This is a nicer try-except
    if 'useremail' in user_data:
        # important that all emails are made lower-cased!
        user_email = user_data['useremail'].lower()
    else: user_email = 'none'

    if 'username' in user_data:
        user_name = user_data['username']
    else: 
        user_name ='Mustermann'
    if 'onesignalid' in user_data:
        user_player_id = user_data['onesignalid']
    else: 
        user_player_id ='0'


    user_hash = hashlib.sha1(user_email).hexdigest()

    #TODO: aBug get_or_create creating new user, because User-Email can change  (19.10.18, Leo)
    #Check: is there a user,
    # IF NO: Create
    # IF YES: Update
    # # Player_id muss überschrieben werden!
    # 


    """  user_check_query = User.select().where(User.user_email == user_email)
    if user_check_query.exists():
        print "USERQUERY: does exist" 
    """
    
    jsondata = {}
    
    user, created = User.get_or_create(
        user_email = user_email,
        #player_id = user_player_id, <-- made a Bug in iOS creating a new User because of always new PlayerID
        defaults={'user_email':user_email,'user_name': user_name, 'hash': user_hash, 'player_id':user_player_id}
        )

    if created == False:
        #send back the Username of the existing user
        jsondata['user_name'] = user.user_name        
        print 'User "{}" did exist'.format(user.user_email)

        if user.player_id != user_player_id:
            print 'Plyer_id changed: {} -> {}'.format(user.player_id,user_player_id)
            user.player_id =  user_player_id
            user.save()   
    
    jsondata['did_exist'] = not created
    jsondata['user_hash'] = user_hash
    

    app.logger.debug(jsondata)
    
    return json.dumps(jsondata)

    '''user, created = User.get_or_create(
        token= a_token,
        username='',
        defaults={'username': "leo-test"})
    '''