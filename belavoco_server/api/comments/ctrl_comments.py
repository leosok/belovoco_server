import models
from models import Comment


@api.route('/comment/<string:hash_value>', methods=['POST'])
def add_comment(hash_value):

    current_user = authorize_user_from_header(request)

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

