from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort, response
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from flask_jwt_extended import create_access_token, get_jwt,jwt_required,get_jwt_identity
from sqlalchemy.sql import func
import hashlib

from db import db
from models import RatingModel
from schemas import RatingSchema, AverageRatingSchema


blp = Blueprint("ratings", __name__, description ="Operations on ratings")

#get rating by rating id
@blp.route("/rating/<string:rating_id>")
class Rating(MethodView):
    @blp.response(200, RatingSchema(many=True))
    def get(self, rating_id):
        rating = RatingModel.query.get_or_404(rating_id)
        return rating
    def delete(self, rating_id):
        rating = RatingModel.query.get_or_404(rating_id)
        raise NotImplementedError("Not implemented")

@blp.route("/avgrating/<int:movie_id>")
class Rating(MethodView):
    @blp.response(200,AverageRatingSchema)
    def get(self, movie_id):
        rating =db.session.query(func.avg(RatingModel.rating).label('Average')).filter(RatingModel.movie_id==movie_id).first()
        response = dict(rating=rating)
        return response

@blp.route("/rating")
class RatingList(MethodView):
    @blp.response(200, RatingSchema(many=True))
    def get(self):
        return RatingModel.query.all()
    @jwt_required()
    @blp.arguments(RatingSchema)
    @blp.response(201, RatingSchema)
    def post(cls, rating_data):
            jwt = get_jwt()
            if not jwt.get("is_admin") or get_jwt_identity()!=rating_data["user_id"]:
                abort(401, message = "Permission denied")
            rating = RatingModel(**rating_data)
            try:
                db.session.add(rating)
                db.session.commit()
            except SQLAlchemyError:
                abort(500, message= "An error occurred while inserting the rating")
            return rating

