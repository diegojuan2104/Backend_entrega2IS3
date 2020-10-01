import sqlite3
from flask_restful import Resource,reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (create_access_token, create_refresh_token,
 jwt_refresh_token_required, get_jwt_identity)


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password', type=str, required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('preferences', type=str, required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('email', type=str, required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('name', type=str, required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('lastname', type=str, required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('user_image_url', type=str, required=True,
                        help="This field cannot be left blank!")

    def post(self):
        data = UserRegister.parser.parse_args()

        if(UserModel.find_by_email(data['email']) == None):
            user = UserModel(**data)  # To completely pass the dictionarie
            user.save_to_db()
        else:
            raise Exception ("correo ya existe")

        return {"message": "User created sucessfully!"}, 201


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('preferences', type=str, required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('email', type=str, required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('name', type=str, required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('lastname', type=str, required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('user_image_url', type=str, required=True,
                        help="This field cannot be left blank!")

    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json()

    def put(self, user_id):
        data = User.parser.parse_args()
        user = UserModel.find_by_id(user_id)

        if User is None:
            return{"mesagge": "An error ocurred"}, 500
        else:
            user.email = data['email']
            user.preferences = data['preferences']
            user.name = data['name']
            user.lastname = data['lastname']
            user.user_image_url = data['user_image_url']
            
            user.save_to_db()

        return user.json()

    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.delete_from_db()
        return {"message": "user deleted"}, 200


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank!")

    def post(self): #with .self it's the same
        # get data from parser 
        data = UserLogin.parser.parse_args()
        # find user in db
        user = UserModel.find_by_email(data['email'])
        # check password

        if user and safe_str_cmp(user.password,data['password']):
            access_token = create_access_token(identity=user.id,fresh=True)
            refresh_token = create_refresh_token(user.id)
            return{
                'user_id':user.id,
                'access_token':access_token,
                'refresh_token':refresh_token
            },200

        return {'message':'invalid credentials'},401

class UserChangePassword(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('new_password', type=str, required=True, help="This field cannot be left blank!")
    

    def put(self):
        data = UserChangePassword.parser.parse_args()
        # find user in db
        user = UserModel.find_by_id(data['user_id'])
        # check password
        if user and safe_str_cmp(user.password,data['password']):
            user.password = data['new_password']
            user.save_to_db()
            return{
                'password_changed':True,
            },200
        
        return {'message':'invalid credentials'},401


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity = current_user)
        return {'access_token':new_token}, 200
