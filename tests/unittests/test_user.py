"""Unit tests for user related functions and methods."""
from unittest import TestCase

from bcrypt import checkpw
from jwt import decode

from api.models import User, secret


class TestUser(TestCase):
    """Testcase for user related functions."""

    def test_user_serialization_should_encrypt_password(self):
        """Validates that the serialization encrypts the given password"""
        data = {
            'username': 'testuser',
            'email': 'testuser@test.test',
            'password': 'secret'
        }
        usr = User(**data)
        self.assertNotEqual(data['password'], usr.password_hash)

    def test_password_hash_should_match_given_string(self):
        """
        Validates that bcrypt is able to match the given string to it's hash.
        """
        data = {
            'username': 'testuser',
            'email': 'testuser@test.test',
            'password': 'secret'
        }
        usr = User(**data)
        encoded_pw = data['password'].encode('utf-8')
        self.assertTrue(checkpw(encoded_pw, usr.password_hash))

    def test_user_token_should_be_generated_with_the_user_id(self):
        """Validates that the generated token have the right configuration."""
        data = {
            'username': 'testuser',
            'email': 'testuser@test.test',
            'password': 'secret'
        }
        usr = User(**data)
        token = usr.generate_token()
        decoded = decode(token, secret, algorithms=['HS256'])
        self.assertEqual(decoded['user'], usr.id)

    def test_user_authentication_should_return_token_when_password_is_valid(self):  # NOQA
        """
        Validates that the authentication method returns a token when the
        right credentials are given.
        """
        data = {
            'username': 'testuser',
            'email': 'testuser@test.test',
            'password': 'secret'
        }
        usr = User(**data)
        token = usr.authenticate(data['password'])
        self.assertIsNotNone(token)

    def test_user_authentication_should_not_return_token_when_password_is_invalid(self):  # NOQA
        """
        Validates that the authentication method returns None when the
        wrong credentials are given.
        """
        data = {
            'username': 'testuser',
            'email': 'testuser@test.test',
            'password': 'secret'
        }
        usr = User(**data)
        token = usr.authenticate('invalid')
        self.assertIsNone(token)
