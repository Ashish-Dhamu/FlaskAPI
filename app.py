from flask import Flask
from flask_restful import Api, reqparse
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.store import Store, StoreList
from resources.item import Item, ItemList
import os



print("first api running")

#JWT : Json Web Token
app = Flask(__name__)
app.secret_key = 'mySecretKey'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL','sqlite:///api.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # 
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth



api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
#api.add_resource(Student, '/student1')

if __name__== "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)

