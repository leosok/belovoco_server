
from flask import Blueprint

# BLUEPRINT #####################
api = Blueprint('api', __name__)
from flask import current_app as app
# BLUEPRINT #####################

from playhouse.shortcuts import model_to_dict


from belavoco_server.models import Audiofile, User

from flask import jsonify
from flask import send_file, request
import json
import simplejson
import os, sys


import logging

@api.route("/")
def api_hello():
    return "Welcome to BeloVoco JSON-Api"

@api.route("/get/<string:hash_value>", methods=['GET'])
@api.route('/get/<string:hash_value>/<string:action>', methods=['GET'])
def get_json(hash_value,action=None):
  
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
                return send_file(file_path)

            else: 
                return json.dumps(data, indent=4, sort_keys=True, default=str)

        #except:
            #return json.dumps(False)    
        #There is a hash comming, we want a file

#ToDo: this will only work it Users alows Push - i think!

@api.route('/set/<string:hash_value>/<string:action>', methods=['GET'])
def set_like(hash_value,action=None):
    this_audio = Audiofile.select().where(Audiofile.hash == hash_value).get()
    if action == 'like':
        #Add +1 to the Play Counter:
        this_audio.times_liked += 1
        this_audio.save()
    
    if action == 'unlike':
        #Add +1 to the Play Counter:
        this_audio.times_liked += 1
        this_audio.save()

    data = model_to_dict (this_audio)
    return json.dumps(data, indent=4, sort_keys=True, default=str)



@api.route("/users/<something>", methods=['GET'])
def user_stub(something):
    return "this is user API"

@api.route("/users/add", methods=['POST'])
def set_user():

    

    #This was not working due to a BUG on PythonAnywhere
    #data = request.get_json(force=False, silent=False)
     
    #Was replaced by:
    data2=request.json.get('token')

    a_token = request.json.get('token')['value']
    a_username = request.json.get('user')['username']

    """  print a_token
    print a_username """

    user, created = User.get_or_create(
    token = a_token,
    username = a_username,
    defaults={'token':a_token,'username': a_username})
   
    jsondata = {}
    jsondata['did_exist'] = not created

    app.logger.debug(jsondata)
    
    return json.dumps(jsondata)

    '''user, created = User.get_or_create(
        token= a_token,
        username='',
        defaults={'username': "leo-test"})
    '''