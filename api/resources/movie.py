from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from flask_jwt_extended import create_access_token, get_jwt,jwt_required,get_jwt_identity

from db import db
from models import MovieModel
from schemas import MovieSchema


blp = Blueprint("movies", __name__, description ="Operations on movies")

@blp.route("/movie/<string:movie_id>")
class movie(MethodView):
    @blp.response(200, MovieSchema)
    def get(self, movie_id):
        movie = MovieModel.query.get_or_404(movie_id)
        return movie
    def delete(self, movie_id):
        movie = MovieModel.query.get_or_404(movie_id)
        db.session.delete(movie)
        db.session.commit()
        return {"message":"Movie deleted"}, 200


@blp.route("/moviename/<string:moviename>")
class movie(MethodView):
    @blp.response(200, MovieSchema(many=True))
    def get(self, moviename):
        print("Looking for "+ moviename)
        return db.session.query(MovieModel).filter(MovieModel.name == moviename)
    
    @jwt_required()
    def delete(self, moviename):
        print("Looking for "+ moviename)
        jwt = get_jwt()
        if not jwt.get("is_admin") :
            abort(401, message = "Permission denied")
        db.session.query(MovieModel).filter(MovieModel.name == moviename).delete(synchronize_session=False)
        db.session.commit()
        return {"message":"Movie deleted"}, 200
        
@blp.route("/movie")
class movieList(MethodView):
    @blp.response(200, MovieSchema(many=True))
    def get(self):
        return MovieModel.query.all()
    @jwt_required()
    @blp.arguments(MovieSchema)
    @blp.response(201, MovieSchema)
    def post(cls, movie_data):
            movie = MovieModel(**movie_data)
            if(movie.year>2050 or movie.year<1888):
                abort(401, message = "Invalid Date")
            db.session.add(movie)
            db.session.commit()
            
    @jwt_required()
    @blp.arguments(MovieSchema)
    @blp.response(200, MovieSchema)
    def put(cls, movie_data):
            moviequery = db.session.query(MovieModel).filter(MovieModel.name == movie_data["name"]).first()
            moviequery = MovieModel(**movie_data)
            if(moviequery.year>2050 or moviequery.year<1888):
                abort(401, message = "Invalid Date")
            db.session.add(moviequery)
            db.session.commit()
            return {"message":"Movie edited successfully."},201
    