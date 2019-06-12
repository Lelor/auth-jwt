"""Unit tests for user related functions and methods."""
from unittest import TestCase

from jwt import decode
from werkzeug.security import check_password_hash

from api.models import User, secret


class TestUser(TestCase):
    """Testcase for user related functions."""

    def test_user_should_encrypt_password(self):
        """Validates that the serialization encrypts the given password"""
        data = {
            'username': 'testuser',
            'email': 'testuser@test.test',
            'password': 'secret',
            'birthdate': '2019-06-12T17:10:42.917178'
        }
        usr = User(**data)
        usr.hash_password()

        self.assertNotEqual(data['password'], usr.password)

    def test_password_hash_should_match_given_string(self):
        """
        Validates that blowfish is able to match the given string to it's hash.
        """
        data = {
            'username': 'testuser',
            'email': 'testuser@test.test',
            'password': 'secret',
            'birthdate': '2019-06-12T17:10:42.917178'
        }
        usr = User(**data)
        usr.hash_password()
        self.assertTrue(check_password_hash(usr.password, data['password']))

    def test_user_token_should_be_generated_with_the_user_id(self):
        """Validates that the generated token have the right configuration."""
        data = {
            'username': 'testuser',
            'email': 'testuser@test.test',
            'password': 'secret',
            'birthdate': '2019-06-12T17:10:42.917178'
        }
        usr = User(**data)
        usr.hash_password()
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
            'password': 'secret',
            'birthdate': '2019-06-12T17:10:42.917178'
        }
        usr = User(**data)
        usr.hash_password()
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
            'password': 'secret',
            'birthdate': '2019-06-12T17:10:42.917178'
        }
        usr = User(**data)
        usr.hash_password()
        token = usr.authenticate('invalid')
        self.assertIsNone(token)
