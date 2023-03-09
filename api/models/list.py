from db import db

class ListModel(db.Model):
    __tablename__ = "lists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(256), nullable =True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=False, nullable=True
    )
    users = db.relationship("UserModel", back_populates="lists")
    listed_movies = db.relationship("ListingModel", back_populates="lists",lazy="dynamic", cascade= "all, delete")