


from belavoco_server import app


if __name__ == '__main__':
    app.run(debug=True,host= 'localhost')
    
    #remove_dead_files(app.config['UPLOAD_FOLDER'])
    