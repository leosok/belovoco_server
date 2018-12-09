# -*- coding: utf-8 -*-

from belavoco_server.models import Audiofile, User
from flask import current_app 
import onesignal as onesignal_sdk



def configure_onesignal():
    config = current_app.config
    onesignal_client = onesignal_sdk.Client(
                            user_auth_key=config['ONESIGNAL_USER_AUTH_KEY'],
                            app={
                                "app_auth_key": config['ONESIGNAL_APP_AUTH_KEY'],
                                "app_id": config['ONESIGNAL_APP_ID']})
    return onesignal_client



def inform_admins(new_user):
   
    admins = current_app.config['ADMIN_EMAILS']
    

    try:
        onesignal_client = configure_onesignal()    
        message = u"{} hat sich soeben neu angemeldet!".format(new_user.user_email)
        
        # create a notification
        push_notification = onesignal_sdk.Notification(contents={"en": message})
        push_notification.set_parameter("headings", {"en": "Neuer User"})

    

        target_devices_array = []

        for admin_mail in admins:        
            admin_push_id = User.select().where(User.user_email == admin_mail).get().player_id
            print admin_push_id
            target_devices_array.append (admin_push_id)
            #target_devices_array.append(user.player_id)

            #print target_devices_array
        push_notification.set_target_devices(target_devices_array)

        # send notification, it will return a response
        onesignal_response = onesignal_client.send_notification(push_notification)
        #print(onesignal_response.status_code)
        print(onesignal_response.json())
    except:
        return False



def push_one(a_user, a_message, a_titel = "Neues Audio"):
    config = current_app.config   
    
    message = a_message.encode('utf-8')

    print "Sending ONE Message to {}:".format(a_user.user_email).encode('utf-8')
    # Encoding will fix Error on Server, leading to not sending PUSH


    onesignal_client = configure_onesignal()    
    
    # create a notification
    push_notification = onesignal_sdk.Notification(contents={"en": a_message})
    push_notification.set_parameter("headings", {"en": a_titel})

    #create array of devices to push to
    target_devices_array=[]
    target_devices_array.append(a_user.player_id)

    #print target_devices_array
    push_notification.set_target_devices(target_devices_array)

    # send notification, it will return a response
    onesignal_response = onesignal_client.send_notification(push_notification)
    #print(onesignal_response.status_code)
    return onesignal_response.json()


#Will send a Push Notif to all users
def push_gun(audiofile):
    config = current_app.config   
    
    message = u"{} von {} wurde hochgeladen! Gelesen hat {}.".format(audiofile.title, audiofile.author, audiofile.reader).encode('utf-8')

    if config['SEND_PUSH'] == False:
        print "SEND_PUSH = FALSE | Not sending Message:"
        # Encoding will fix Error on Server, leading to not sending PUSH
        #print message.encode('utf-8')
    
    else:

        print "Sending Message:"
        # Encoding will fix Error on Server, leading to not sending PUSH
        #print message.encode('utf-8')

        onesignal_client = configure_onesignal()    
        
        # create a notification
        push_notification = onesignal_sdk.Notification(contents={"en": message})
        push_notification.set_parameter("headings", {"en": "Neues Audio"})

        #create array of devices to push to
        target_devices_array = []
        for user in User.select().where(User.player_id <> "0"):
            target_devices_array.append(user.player_id)

        #print target_devices_array
        push_notification.set_target_devices(target_devices_array)

        # send notification, it will return a response
        onesignal_response = onesignal_client.send_notification(push_notification)
        #print(onesignal_response.status_code)
        print(onesignal_response.json())


if __name__ == "__main__":
    print "started"