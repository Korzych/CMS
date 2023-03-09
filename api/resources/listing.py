from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from flask_jwt_extended import jwt_required, get_jwt,get_jwt_identity

from db import db
from models import MovieModel, ListingModel, ListModel
from schemas import MovieSchema, ListingSchema


blp = Blueprint("listed_movies", __name__, description ="Operations on listed movies")

@blp.route("/listing/<int:listing_id>")
class listing(MethodView):
    @blp.response(200, ListingSchema)
    def get(self, listing_id):
        listing = ListingModel.query.get_or_404(listing_id)
        return listing
    def delete(self, listing_id):
        listing = ListingModel.query.get_or_404(listing_id)
        db.session.delete(listing)
        db.session.commit()

@blp.route("/listing/<int:listing_id>")
class listing(MethodView):
    blp.response(200, ListingSchema)
    def delete(self, listing_id):
        movie = ListingModel.query.get_or_404(listing_id)
        db.session.delete(movie)
        db.session.commit()


@blp.route("/listing")
class listing(MethodView):
    @blp.arguments(ListingSchema)
    @blp.response(201, ListingSchema)
    @jwt_required()
    def post(cls, listing_data):
            listing = ListingModel(**listing_data)
            list = ListModel.query.get_or_404(listing.list_id)
            jwt = get_jwt()
            if not jwt.get("is_admin") and get_jwt_identity()!=list.user_id:
                abort(401, message = "Permission denied")
            db.session.add(listing)
            db.session.commit()

            return listing

    @blp.response(200, ListingSchema(many=True))
    def get(self):
        return ListingModel.query.all()

