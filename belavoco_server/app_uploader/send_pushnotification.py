from exponent_server_sdk import DeviceNotRegisteredError
from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushResponseError
from exponent_server_sdk import PushServerError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError

from belavoco_server.models import Audiofile, User


#Will send a Push Notif to all users
def push_gun(audiofile):

    message = "{} von {} wurde hochgeladen! Gelesen hat {}.".format(audiofile.title, audiofile.author, audiofile.reader)
    print message
    #This function is not used, because Expo was dropped. It is still here as a starting point for notifications.   
    ''' for user in User.select():        
        send_push_message(user.token, message)
    '''
