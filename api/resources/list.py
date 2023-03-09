from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required, get_jwt,get_jwt_identity

from db import db
from models import ListModel, ListingModel
from schemas import ListUpdateSchema, ListSchema, ListingSchema

blp = Blueprint("Lists", "lists", description="Operations on lists")


@blp.route("/list/<int:list_id>")
class List(MethodView):
    @jwt_required()
    @blp.response(200, ListSchema)
    def get(self, list_id):
        list = ListModel.query.get_or_404(list_id)
        return dict(id = list.id ,name = list.name, description = list.description, user_id= list.user_id)

    @jwt_required()
    def delete(self, list_id):
        jwt = get_jwt()
        list = ListModel.query.get_or_404(list_id)
        if not jwt.get("is_admin") and get_jwt_identity()!=list.user_id:
            abort(401, message = "Permission denied")
        db.session.delete(list)
        db.session.commit()
        return {"message":"List deleted"}, 200

@blp.route("/listedmovies/<int:list_id>")
class MovieList(MethodView):
    @jwt_required()
    @blp.response(200, ListingSchema(many=True))
    def get(self, list_id):
        listing = ListingModel.query.filter(ListingModel.list_id == list_id)
        return listing

@blp.route("/list")
class ListList(MethodView):
    @blp.response(200, ListSchema(many=True))
    def get(self):
        return ListModel.query.all()
    @jwt_required()
    @blp.arguments(ListSchema)
    @blp.response(201, ListSchema)
    def post(self,list_data):
        list = ListModel(**list_data)
        if(ListModel.query.filter(ListModel.name == list_data["name"]).filter(ListModel.user_id == get_jwt_identity()).first()):
            abort(409, message ="List with that name already exists")
        try:
            db.session.add(list) 
            db.session.commit()
        except IntegrityError:
            abort(400, message= "Integrity error")

        except SQLAlchemyError:
            abort(500, message= "An error occurred while inserting the list")

        return list

@blp.route("/list/<string:username>")
class ListList(MethodView):
    @blp.response(200, ListSchema(many=True))
    def get(self):
        return ListModel.query.all()