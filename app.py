from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister,User,UserLogin,UserChangePassword

app = Flask(__name__) #This means that this it's the main doc where flask runs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # To locate the db doc, and add sqlite,postgreSQL,Oracle whatever....
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Modification tracker
api = Api(app) #Allow add Resources from flask Rest-full
app.secret_key = 'abcd'

@app.before_first_request #To Create all the tables before run 
def create_tables():
    db.create_all()

jwt = JWTManager(app)  #JWTManager It doesn't creating /auth endpoint

#USER ROUTES
api.add_resource(UserRegister,'/register')
api.add_resource(User,'/user/<int:user_id>')
api.add_resource(UserLogin,'/login')
api.add_resource(UserChangePassword,'/user/changePassword')


# Allows only run in app.py
if __name__ == '__main__':
    from db import db 
    db.init_app(app)
    app.run(port = 3000, debug=True)