#uploader_belovoco.py
# -*- coding: utf-8 -*-

import traceback
import os

import peewee 
from mutagen.mp3 import MP3
from belavoco_server.models import Audiofile
from file_hashing import hash_file

def create_audio_decription(audiofile):
    try:
        audio = MP3(audiofile)
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
                    text_lang = request.form.get("text_lang")
                )    
    
        
            new_audiofile.save
        
        except peewee.IntegrityError as e:
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