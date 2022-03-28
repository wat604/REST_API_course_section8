import os

from flask import Flask, request, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token

from security import authenticate
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
# from db import db

uri = os.getenv("DATABASE_URL", "sqlite://data.db")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "bjaoibf"
jwt = JWTManager(app)

api = Api(app)

# Create a route to authenticate your users and return JWTs.
# The create_access_token() functin is used to actually generate the JWT
@app.route("/auth", methods=["POST"])
def auth():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = authenticate(username, password)
    if not user:
        return jsonify({"msg": "Bad username or password"}), 401
    
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)



api.add_resource(UserRegister, '/register')
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/item/chair
api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/store/<string:name>')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)



