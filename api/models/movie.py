from db import db

class MovieModel(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(80), unique=False, nullable=False)
    year =db.Column(db.Integer, unique=False, nullable=False)
    category = db.Column(db.String(64), unique = False, nullable= True)
    image = db.Column(db.String(16777215), unique = False, nullable= True)
    listed_movies = db.relationship("ListingModel", back_populates="movies", lazy="dynamic",cascade= "all, delete")
    ratings = db.relationship("RatingModel", back_populates="movies", lazy="dynamic",cascade= "all, delete")