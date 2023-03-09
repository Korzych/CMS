from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, get_jwt,jwt_required,get_jwt_identity
from passlib.hash import pbkdf2_sha256

from db import db
from blocklist import BLOCKLIST
from models import UserModel
from schemas import UserSchema


blp = Blueprint("users", __name__, description ="Operations on users")

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    @jwt_required()
    def delete(self, user_id):
        jwt = get_jwt()
        if not jwt.get("is_admin") and get_jwt_identity()!=user_id:
            abort(401, message = "Permission denied")
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message":"User deleted"}, 200
        
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user


@blp.route("/username/<string:user>")
class User(MethodView):
    @blp.response(200, UserSchema(many=True))
    #Get user by username 
    def get(self, user):
        print("Looking for "+ user)
        userObject = db.session.query(UserModel).filter(UserModel.username == user)
        if userObject.count() == 0:
            return {"message": "Not Found."}, 404
        return userObject
    @blp.response(202, UserSchema(many=True))
    @jwt_required()
    #Delete user only for admin
    def delete(self, user):
        jwt = get_jwt()
        if not jwt.get("is_admin") :
            abort(401, message = "Permission denied")
        db.session.query(UserModel).filter(UserModel.username == user).delete(synchronize_session=False)
        db.session.commit()
        return {"message":"User deleted"}, 200


@blp.route("/user")
class User(MethodView):
    @jwt_required()
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    #Edit user
    def put(cls,user_data):
        jwt = get_jwt()
        user = db.session.query(UserModel).filter(UserModel.username == user_data["username"]).first()
        if(user_data["is_admin"]):
            if not jwt.get("is_admin") :
                abort(401, message = "Permission denied")
            user.is_admin = user_data["is_admin"]
        
        user.username = user_data["username"]
        user.password = pbkdf2_sha256.hash(user_data["password"])
        db.session.add(user)
        db.session.commit()
        return {"message":"User Edited"}, 200


@blp.route("/user")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()
    
@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if(UserModel.query.filter(UserModel.username == user_data["username"]).first()):
            abort(409, message ="User with that name already exists")
        if(user_data["username"]==""):
            abort(401,message= "Invalid credentials.")
        user = UserModel(**user_data)
        user.password = pbkdf2_sha256.hash( user.password)
        user.is_admin = False
        db.session.add(user)
        db.session.commit()

        return {"message":"User created successfully."},201

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post (self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}
        abort(401,message= "Invalid credentials.")

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message":"Successfully logged out."}

class LoginHelper:
    def is_admin(id):
        userObject = db.session.query(UserModel).filter(UserModel.id == id).filter(UserModel.is_admin == True)
        if userObject.count() != 0:
            return True
        else: 
            return False