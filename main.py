import logging
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from constants import *

from flask_sqlalchemy import SQLAlchemy
logging.basicConfig(filename=FILE_NAME_LOG, level=logging.DEBUG)

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(256), unique=False, nullable=False)
    cuenta_usuario = db.Column(db.String(256), unique=False, nullable=False)
    fecha_cese = db.Column(db.DateTime, nullable=True)
    numero_ticket = db.Column(db.String(256), unique=False, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nombre_usuario} - {self.numero_ticket}>'

@app.before_first_request
def create_tables():
    db.create_all()

class webhook(Resource):
    def get(self):
        response = {"IP": request.remote_addr , "HOST": request.host, "URL": request.url, "METHOD": request.method}
        logging.info(f'WEBHOOK GET: {response}')
        return response
    def post(self):
        response = {"IP": request.remote_addr , "HOST": request.host, "URL": request.url, "METHOD": request.method}
        if request.data:
            response['BODY']= request.json
            logging.info(f'WEBHOOK POST: {response}')
            return jsonify(response)
        response['ERROR'] = {"ERROR":"BODY NOT FOUND"}
        logging.info(f'WEBHOOK POST: {response}')
        return response['ERROR']


class Usuarios(Resource):
    def get(self):
        ret = []
        res = Usuario.query.all()
        for user in res:
            ret.append(
                {
                    'nombre_usuario': user.nombre_usuario,
                    'fecha_cese': user.fecha_cese,
                    'numero_ticket': user.numero_ticket,
                    'cuenta_usuario': user.cuenta_usuario
                }
            )
        return ret, 200


api.add_resource(Usuarios, '/usuarios/')
api.add_resource(webhook, '/webhook/')

if __name__ == '__main__':
    app.run(host=HOSTS[HOST_NUMBER],port=PORT, debug=DEBUG_MODE)
