from db import db

class RatingModel(db.Model):
    __tablename__ = "ratings"

    id = db.Column(db.Integer, primary_key=True)
    movie_id =  db.Column(
        db.Integer, db.ForeignKey("movies.id"), unique=False, nullable=False
    )
    user_id =  db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False
    )
    rating = db.Column(db.Integer, unique = False, nullable = False)
    users = db.relationship("UserModel", back_populates="ratings")
    movies = db.relationship("MovieModel", back_populates="ratings")