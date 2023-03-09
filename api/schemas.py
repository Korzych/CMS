from marshmallow import Schema, fields, ValidationError

class PlainListSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)

class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    is_admin = fields.Boolean(partial=True)

class PlainListingSchema(Schema):
    id = fields.Int(dump_only=True)
    place_on_the_list = fields.Int(required = True)

class PlainMovieSchema(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str(required= True)
    year = fields.Int(required = True)
    category = fields.Str(required=False)
    image = fields.Str(required =False)

class PlainRatingSchema(Schema):
    id = fields.Int(dump_only=True)
    rating = fields.Int(required = True)

class ListSchema(PlainListSchema):
    user_id = fields.Int(required=False, load_only=False)
    user = fields.Nested(PlainUserSchema(), dump_only=True)
    listed_movies = fields.Nested(PlainListingSchema())

class ListUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()

class UserSchema(PlainUserSchema):
    lists = fields.List(fields.Nested(PlainListSchema()), dump_only=True)
    ratings = fields.List(fields.Nested(PlainRatingSchema()),dump_only= True)

class MovieSchema(PlainMovieSchema):
    listed_movies = fields.List(fields.Nested(PlainListingSchema()), dump_only=True)
    ratings = fields.List(fields.Nested(PlainRatingSchema()),dump_only= True)

class RatingSchema(PlainRatingSchema):
    user_id = fields.Int(required = True, load_only=False)
    user = fields.Nested(PlainUserSchema(),dump_only=True)
    movie_id = fields.Int(required= True, load_only = False)
    movie = fields.Nested(PlainMovieSchema(),dump_only = True)

class ListingSchema(PlainListingSchema):
    list_id =fields.Int(required = True, load_only=False)
    list = fields.Nested(PlainListSchema(),dump_only=True)
    movie_id = fields.Int(required= True, load_only = False)
    movie = fields.Nested(PlainMovieSchema(),dump_only = True)

