from schema import Schema, And

from flask_marshmallow import Marshmallow

ma = Marshmallow()

user_registration_validator = Schema([{'username': str,
                                       'email': str,
                                       'password': str}])
user_auth_validator = Schema([{'username': str,
                               'password': str}])

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'email')


user_schema = UserSchema()
users_schema = UserSchema(many=True)