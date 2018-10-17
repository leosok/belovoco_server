
from flask import Blueprint

# BLUEPRINT #####################
api = Blueprint('api', __name__)
from flask import current_app as app
# BLUEPRINT #####################

from playhouse.shortcuts import model_to_dict


from belavoco_server.models import Audiofile, User

from flask import jsonify
from flask import send_file, request, Response
import json
import simplejson
import os, sys
import re
import mimetypes
from werkzeug.security import generate_password_hash


import logging
import hashlib
from peewee import DoesNotExist

def play_seeking(path, the_request):

    range_header = the_request.headers.get('Range', None)
    print the_request.headers
    if not range_header:
        print "just sending a file"
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


def authorize_user_from_header(rq):
    
    try:
        #Checking if there is a AUTH-Header, if not this will throw a KeyError
        request_user_hash = rq.headers['Authorization']
        try:
            #Checking ig a user with this Hash exists, and returns it if found
            this_user = User.select().where(User.hash == request_user_hash).get()
            print "Authorized request: %s" % this_user.user_email            
            return this_user
        except DoesNotExist:
            print "User not found. Hash: '%s'" % request_user_hash
            return False
    except KeyError:   
        print "Using old API, without Authorization-Header"
        return False


@api.route("/")
def api_hello():
    return "Welcome to BeloVoco JSON-Api"

@api.route("/get/<string:hash_value>", methods=['GET'])
@api.route('/get/<string:hash_value>/<string:action>', methods=['GET'])
def get_json(hash_value,action=None):
  
    authorize_user_from_header(request)
   
    if hash_value == 'all':

        all_records = []
        for a in Audiofile.select().order_by(Audiofile.upload_time.desc()):
            a_dict = model_to_dict(a)
            all_records.append(a_dict)
        

        return json.dumps(all_records, indent=4, sort_keys=True, default=str)
        #return simplejson.dumps({filename: 'True'})

    else:
        #try:
            this_audio = Audiofile.select().where(Audiofile.hash == hash_value).get()
            data = model_to_dict (this_audio)
            if action == 'play':
                #Add +1 to the Play Counter:
                this_audio.times_played += 1
                this_audio.save()
                
                #Create path & send the file to User
                file_path = os.path.join(app.root_path,'..',this_audio.file_name)
                return play_seeking(file_path,request)
               

            else: 
                return json.dumps(data, indent=4, sort_keys=True, default=str)

        #except:
            #return json.dumps(False)    
        #There is a hash comming, we want a file

@api.route('/set/<string:hash_value>/<string:action>', methods=['GET','POST'])
def set_like(hash_value,action=None):
    this_audio = Audiofile.select().where(Audiofile.hash == hash_value).get()
    
    #I am getting a Post request with a UserHash
    #TODO: Implement User-Model wich will get the likes instad of the audiofiles! 
    #print request.get_json()
    
    authorize_user_from_header(request)


    if action == 'like':
        
        this_audio.times_liked += 1
        this_audio.save()
    
    if action == 'unlike':
       
        if this_audio.times_liked > 0:
            this_audio.times_liked -= 1
            this_audio.save()

    data = model_to_dict (this_audio)
    return json.dumps(data, indent=4, sort_keys=True, default=str)



@api.route("/user/<something>", methods=['GET'])
def user_stub(something):
    return "this is user API"

@api.route("/user/add", methods=['POST','PUT'])
def set_user():
    
    if flask.request.method == 'PUT':
        print "Updating User..."
        return "User Updated"

    
    if flask.request.method == 'POST':
    #This was not working due to a BUG on PythonAnywhere
    #data = request.get_json(force=False, silent=False)
     
    #Was replaced by:
        data2 = request.json.get('user')
        print data2

        #This is a nicer try-except
        if 'useremail' in request.json.get('user'):
            user_email = request.json.get('user')['useremail']
        else: user_email = 'none'

        if 'username' in request.json.get('user'):
            user_name = request.json.get('user')['username']
        else: 
            user_name ='Mustermann'
        if 'playerid' in request.json.get('user'):
            user_player_id = request.json.get('user')['playerid']
        else: 
            user_player_id ='0'


        user_hash = hashlib.sha1(user_email).hexdigest()

        user, created = User.get_or_create(
            user_email = user_email,
            player_id = user_player_id,
            defaults={'user_email':user_email,'user_name': user_name, 'hash': user_hash, 'player_id':user_player_id}
            )
    
        jsondata = {}
        jsondata['did_exist'] = not created
        jsondata['user_hash'] = user_hash

        app.logger.debug(jsondata)
        
        return json.dumps(jsondata)

        '''user, created = User.get_or_create(
            token= a_token,
            username='',
            defaults={'username': "leo-test"})
        '''