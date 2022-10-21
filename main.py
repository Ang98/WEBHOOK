import logging
from flask import Flask, request, jsonify
from constants import *

logging.basicConfig(filename=FILE_NAME_LOG, level=logging.DEBUG)

app = Flask(__name__)


@app.route('/webhook/', methods = ['GET','POST'])
def webhook():
    response = {"IP": request.remote_addr , "HOST": request.host, "URL": request.url, "METHOD": request.method}
    if request.method == 'GET':
        logging.info(f'WEBHOOK GET: {response}')
        return response
    if request.method == 'POST':
        if request.data:
            response['BODY']= request.json
            logging.info(f'WEBHOOK POST: {response}')
            return jsonify(response)
        response['ERROR'] = {"ERROR":"BODY NOT FOUND"}
        logging.info(f'WEBHOOK POST: {response}')
        return response['ERROR']


if __name__ == '__main__':
    app.run(host=HOSTS[HOST_NUMBER],port=PORT, debug=DEBUG_MODE)