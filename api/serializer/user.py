"""Module of schema validators to be used on the routes."""
from flask_marshmallow import Marshmallow
from marshmallow import fields

from api.models import User, Movie, MovieGenre


ma = Marshmallow()


def configure(app):
    """Initializes the application on the marshmallow instance."""
    ma.init_app(app)


class UserSchema(ma.ModelSchema):
    """Schema for user serialization."""
    class Meta:
        """Class to dump on serialization."""
        model = User
        fields = ('username', 'email', 'password', 'birthdate')

    username = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Email(required=True)
    birthdate = fields.DateTime(required=True)


USER_REGISTRATION_SERIALIZER = UserSchema()
USER_AUTH_SERIALIZER = UserSchema(only=('username', 'password'))


class MovieSchema(ma.ModelSchema):
    """Schema for movie serialization."""
    class Meta:
        """Class to dump object on load."""
        model = Movie
        fields = ('name', 'release_date', 'director', 'genre_id', 'picture')
    
    name = fields.Str(required=True)
    release_date = fields.DateTime(required=True)
    director = fields.Str(required=True)
    genre_id = fields.Int(required=True)
    picture = fields.Str(required=True)


MOVIE_SERIALIZER = MovieSchema()


class MovieGenreSchema(ma.ModelSchema):
    class Meta:
        """Class to dump object on load."""
        model = MovieGenre
        fields = ('text',)
    
    text = fields.Str(required=True)


MOVIE_GENRE_SERIALIZER = MovieGenreSchema()
