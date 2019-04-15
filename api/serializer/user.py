"""Module of schema validators to be used on the routes."""
from flask_marshmallow import Marshmallow
from marshmallow import fields

from api.models import User


ma = Marshmallow()


def configure(app):
    """Initializes the application on the marshmallow instance."""
    ma.init_app(app)


class UserSchema(ma.ModelSchema):
    """Schema for user serialization."""
    class Meta:
        """Class to dump on serialization."""
        model = User
        fields = ('username', 'email', 'password')

    username = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Email(required=True)


USER_REGISTRATION_SERIALIZER = UserSchema()
USER_AUTH_SERIALIZER = UserSchema(only=('username', 'password'))
