from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class Usuario(Resource):
    
    def get(self, name):
        return{'name':name}

    def post(self, id):
        pass

api.add_resource(Usuario,'/usuario/<string:name>')


app.run(port=5000)