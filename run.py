


from belavoco_server import app


if __name__ == '__main__':

    context = ('bv_cert.pem', 'bv_key.pem')
    app.run(host='0.0.0.0', port=443, ssl_context=context, threaded=True, debug=True)


    app.config['SEND_PUSH'] = False
    
    #Uncomment for HTTP
    #app.run(debug=True,host= '0.0.0.0', port=8080, ssl_context=context)
