from flask import Blueprint

# BLUEPRINT #####################
api = Blueprint('api', __name__)
from flask import current_app as app
# BLUEPRINT #####################

from playhouse.shortcuts import model_to_dict


from belavoco_server.models import Audiofile, User

from flask import jsonify
from flask import send_file,request
import json
import simplejson
import os

@api.route("/")
def api_hello():
    return "Welcome to BeloVoco JSON-Api"

@api.route("/get/<string:hash_value>", methods=['GET'])
@api.route('/get/<string:hash_value>/<string:action>', methods=['GET'])
def get_json(hash_value,action=None):
  
    if hash_value == 'all':

        all_records = []
        for a in Audiofile.select():
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
@api.route("/users/add", methods=['POST'])
def set_user():

    #print request.get_data()

    data = request.get_json(force=False, silent=False)
    print data

    a_token = data['token']['value']
    a_username = data['user']['username']

    print a_token
    print a_username

    user, created = User.get_or_create(
    token = a_token,
    username = a_username,
    defaults={'token':a_token,'username': a_username})
   
    jsondata = {}
    jsondata['did_exist'] = not created

    print jsondata

    return json.dumps(jsondata)

    '''user, created = User.get_or_create(
        token= a_token,
        username='',
        defaults={'username': "leo-test"})
    '''