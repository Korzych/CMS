from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password =db.Column(db.String(64), unique=False, nullable=False)
    is_admin= db.Column(db.Boolean, unique= False, nullable = False )
    
    lists = db.relationship("ListModel", back_populates="users", lazy="dynamic", cascade= "all, delete")
    ratings = db.relationship("RatingModel", back_populates="users", lazy="dynamic", cascade= "all, delete")