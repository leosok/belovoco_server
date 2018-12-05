#uploader_belovoco.py
# -*- coding: utf-8 -*-

import traceback
import os

import peewee 
import mutagen


from belavoco_server.models import Audiofile, User
from file_hashing import hash_file
from send_pushnotification import push_gun

from flask import current_app


def create_audio_decription(audiofile):
    try:
        audio = mutagen.File(audiofile)
        return audio.info.length

    except:
        print traceback.format_exc()
        return False

def save_file_to_db(audiofile, request):
    try:
        
        audio_length = create_audio_decription(audiofile)
        file_size = os.path.getsize(audiofile)       
      
        #create the URL
        file_hash = hash_file(audiofile)

        file_url = '{url}api/get/{hash}/play'.format(url=request.url_root, hash=file_hash)


        print "Creator ist: {}".format(request.form.get("creator_email"))

        try:
            creator_mail = request.form.get("creator_email")
            creator = User.select().where(User.user_email == creator_mail).get()
        except:
            #anonymus; make Admin the user       
            print "Upload with NO USER!"
            creator = User.select().where(User.id == 1).get()

        try:            

            new_audiofile = Audiofile.create(
                    file_name = audiofile,
                    reader = request.form.get("reader"),
                    author=  request.form.get("author"),
                    title=   request.form.get("title"),
                    file_size=file_size,
                    length = audio_length,
                    hash = file_hash,
                    file_url = file_url,
                    text_type = request.form.get("text_type"),
                    text_lang = request.form.get("text_lang"),
                    creator = creator
                )    
    
        
            new_audiofile.save
            

            if creator_mail != current_app.config['SILENT_PUSH_MAIL']:    
                push_gun(new_audiofile)
            else:
                print "(Upload) I was asked to keep SILENT."
        
        except peewee.IntegrityError as e:
            print e
            print "Audiofile Hash is a duplicate!"
            print "Deleting %s" % audiofile
            os.remove(audiofile)

            return False
        

        return True

    except:
        print traceback.format_exc()
        return False


def remove_file_from_db(file):
    global Audiofile
    file_to_remove = Audiofile.select().where(Audiofile.file_name == file).get()
    file_to_remove.delete_instance()

def remove_dead_files(folder):

    files = [os.path.join(folder,f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]

    global Audiofile

    query = Audiofile.select()
    files_audio = [Audiofile.file_name for Audiofile in query]

    #Compare files in DB with existing files
    files_to_remove = set(files).symmetric_difference(set(files_audio))
    print files_to_remove

    try:
        for f in files_to_remove:
            if os.path.exists(f):
                os.remove(f)
            else:
                print f
                remove_file_from_db(f)
        return True
    except:
        print traceback.format_exc()
        return False