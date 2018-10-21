#!flask/bin/python

# Author: Ngo Duy Khanh
# Email: ngokhanhit@gmail.com
# Git repository: https://github.com/ngoduykhanh/flask-file-uploader
# This work based on jQuery-File-Upload which can be found at https://github.com/blueimp/jQuery-File-Upload/

from __future__ import print_function

# BLUEPRINT #####################
from flask import Blueprint

app_uploader = Blueprint('app_uploader', __name__, template_folder='templates')
from flask import current_app as app
# BLUEPRINT #####################




import os

import simplejson
import traceback

from flask import Flask, request, render_template, redirect, url_for, send_from_directory

from werkzeug import secure_filename

from lib.upload_file import uploadfile

from uploader_belavoco import save_file_to_db, remove_dead_files, remove_file_from_db




#ALLOWED_EXTENSIONS = set(['wav','ogg', 'mp3'])
ALLOWED_EXTENSIONS = set(['mp3'])
IGNORED_FILES = set(['.gitignore','.data'])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def gen_file_name(filename):
    """
    If file was exist already, rename it and return a new name
    """

    i = 1
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i += 1

    return filename




@app_uploader.route("/upload", methods=['GET', 'POST'])
def upload():

    #print(request.get_data())

    if request.method == 'POST':
        files = request.files['file']
        
        

        if files:
            filename = secure_filename(files.filename)
            filename = gen_file_name(filename)
            mime_type = files.content_type
            
            print(filename)
            print(allowed_file(files.filename))

            if allowed_file(files.filename) == False:
                result = uploadfile(name=filename, type=mime_type, size=0, not_allowed_msg="File type not allowed")

            else:
                # save file to disk
                uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                files.save(uploaded_file_path)

                # get file size after saving
                size = os.path.getsize(uploaded_file_path)

                # IF AUDIO
                if mime_type.startswith('audio'):
                    #Create Audio-Object & Save it to database       
                    save_file_to_db(uploaded_file_path, request)
                                  
                
                # return json for js call back
                result = uploadfile(name=filename, type=mime_type, size=size)
            
            return simplejson.dumps({"files": [result.get_file()]})

    if request.method == 'GET':
        # get all file in ./data directory
        
        files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'],f)) and f not in IGNORED_FILES ]
        
        file_display = []

        for f in files:
            size = os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], f))
            file_saved = uploadfile(name=f, size=size)
            file_display.append(file_saved.get_file())

        return simplejson.dumps({"files": file_display})

    return redirect(url_for('.index'))


@app_uploader.route("/delete/<string:filename>", methods=['DELETE'])
def delete(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    #file_thumb_path = os.path.join(app.config['THUMBNAIL_FOLDER'], filename)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            remove_file_from_db(file_path)

            #if os.path.exists(file_thumb_path):
            #    os.remove(file_thumb_path)
            
            return simplejson.dumps({filename: 'True'})
        except:
            return simplejson.dumps({filename: 'False'})

@app_uploader.route("/data/<string:filename>", methods=['GET'])
def get_file(filename):
    #return os.path.join('..',app.config['UPLOAD_FOLDER'])
   # return send_from_directory(os.path.join('..',app.config['UPLOAD_FOLDER']),
   #                            filename, as_attachment=True)


    import sys

    path = os.path.join(app.root_path,'..', app.config['UPLOAD_FOLDER'])
    print(path)    
    return send_from_directory(path, filename=filename)



@app_uploader.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

