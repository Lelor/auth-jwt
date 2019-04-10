"""Module of schema validators to be used on the routes."""
from schema import Schema, And


user_registration_validator = Schema({'username': str,
                                      'email': str,
                                      'password': str})
user_auth_validator = Schema({'username': str,
                              'password': str})
