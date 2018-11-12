


from belavoco_server import app


if __name__ == '__main__':
    app.config['SEND_PUSH'] = False
    app.run(debug=True,host= '0.0.0.0', port=8080)
    
    #remove_dead_files(app.config['UPLOAD_FOLDER'])