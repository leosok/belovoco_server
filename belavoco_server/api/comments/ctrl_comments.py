from belavoco_server.api.controllers import *



def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
            if not 'Authorization' in request.headers:
               abort(401)            
            else:            
                request_user_hash = request.headers['Authorization']
                kws['current_user'] = User.select().where(User.hash == request_user_hash).get()
                return f(*args, **kws)            
    return decorated_function


@api.route('/comment/<string:hash_value>', methods=['POST'])
@authorize
def add_comment(hash_value, current_user=None):

    print request.json
    #authorize_user_from_header(request)

    comment_data = request.json.get('comment')

    this_audio = Audiofile.select().where(Audiofile.hash == hash_value).get()
      
    this_audio.create_comment(user=current_user, content = comment_data)


    print "{}, {}".format(current_user.user_name,this_audio.title)    
    """   if action == 'unlike':
       
        if this_audio.times_liked > 0:
            this_audio.times_liked -= 1
            this_audio.save() """

    data = model_to_dict (this_audio)
    return json.dumps(data, indent=4, sort_keys=True, default=str)


@api.route('/comment/<string:hash_value>', methods=['GET'])
@authorize
def get_comments(hash_value, current_user=None):
    
    
    return Audiofile.get_comments_json(Audiofile.get_by_hash(hash_value))


@api.route('/comment/<int:comment_id>', methods=['DELETE'])
@authorize
def delete_comments(comment_id, current_user=None):
    print "DELETING--- USER: %s" % (current_user.user_name)
    Comment.delete_comment(comment_id,current_user)
    return "OK"