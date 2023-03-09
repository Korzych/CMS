from db import db

class ListingModel(db.Model):
    __tablename__ = "listed_movies"

    id = db.Column(db.Integer, primary_key=True)
    movie_id =  db.Column(
        db.Integer, db.ForeignKey("movies.id"), unique=False, nullable=False
    )
    list_id =  db.Column(
        db.Integer, db.ForeignKey("lists.id"), unique=False, nullable=False
    )
    place_on_the_list = db.Column(db.Integer, unique = False, nullable = False)

    lists = db.relationship("ListModel", back_populates="listed_movies")
    movies = db.relationship("MovieModel", back_populates="listed_movies")