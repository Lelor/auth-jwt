"""User actions system tests module."""
from unittest import TestCase

from api import create_app
from api.models import User, engine, Base, session
from api.modules.user import registrate_user


class TestSignUp(TestCase):
    """Sign up tests."""

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SERVER_NAME'] = 'test'
        self.app.session = session
        self.client = self.app.test_client()
        context = self.app.app_context()
        context.push()

        Base.metadata.create_all(engine)

    def tearDown(self):
        self.app.session.remove()
        Base.metadata.drop_all(engine)

    def test_create_user_with_valid_data(self):
        """Validates user creation when the route receives valid data."""
        data = {
            'username': 'testuser',
            'email': 'testuser@test.test',
            'password': 'secret'
        }
        res = self.client.post('/user', json=data)
        query = session.query(User).all()
        self.assertEqual(res.status_code, 201)
        self.assertEqual(len(query), 1)

    def test_create_user_with_invalid_data(self):
        """Validates error when the route receives invalid data."""
        data = {
            'usrname': 'testuser',
            'email': 'testuser@test.test',
            'password': 'secret'
        }
        res = self.client.post('/user', json=data)
        query = session.query(User).all()
        self.assertEqual(res.status_code, 400)
        self.assertEqual(len(query), 0)

    def test_duplicate_user_should_not_be_registered(self):
        """Validates error when sent data is already in database."""
        data = {
            'username': 'testuser',
            'email': 'testuser@test.test',
            'password': 'secret'
        }
        usr = User(**data)
        session.add(usr)
        session.commit()
        res = self.client.post('/user', json=data)
        query = session.query(User).all()
        self.assertEqual(res.status_code, 409)
        self.assertEqual(len(query), 1)


class TestSignIn(TestCase):
    """Authentication tests."""

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SERVER_NAME'] = 'test'
        self.app.session = session
        self.client = self.app.test_client()
        context = self.app.app_context()
        context.push()

        Base.metadata.create_all(engine)

    def tearDown(self):
        self.app.session.remove()
        Base.metadata.drop_all(engine)

    def test_sign_in_with_valid_credentials(self):
        """
        Validates success response on authentication withvalid credentials.
        """
        data = {
            'username': 'testuser',
            'email': 'testuser@test.test',
            'password': 'secret'
        }
        usr = User(**data)
        registrate_user(usr)
        del data['email']
        res = self.client.post('/sign_in', json=data)
        self.assertEqual(res.status_code, 200)

    def test_sign_in_with_invalid_username(self):
        """
        Validates error when authentication fails with invalid username.
        """
        data = {
            'username': 'testuser',
            'email': 'testuser@test.test',
            'password': 'secret'
        }
        invalid_credentials = {'username': 'tstuser',
                               'password': 'secret'}
        usr = User(**data)
        registrate_user(usr)
        res = self.client.post('/sign_in', json=invalid_credentials)
        self.assertEqual(res.status_code, 401)

    def test_sign_in_with_invalid_password(self):
        """
        Validates error when authentication fails with invalid password.
        """
        data = {
            'username': 'testuser',
            'email': 'testuser@test.test',
            'password': 'secret'
        }
        invalid_credentials = {'username': 'testuser',
                               'password': 'scret'}
        usr = User(**data)
        registrate_user(usr)
        res = self.client.post('/sign_in', json=invalid_credentials)
        self.assertEqual(res.status_code, 401)

    def test_get_authenticated_route_with_valid_token(self):
        """Validates that a valid token works on authenticated route."""
        data = {
            'username': 'testuser',
            'email': 'testuser@test.test',
            'password': 'secret'
        }
        usr = User(**data)
        registrate_user(usr)
        token = usr.generate_token()
        res = self.client.get('/secret', headers={'auth-token': token})
        self.assertEqual(res.status_code, 200)

    def test_get_authenticated_route_with_invalid_token(self):
        """
        Validates that an invalid token doesn't work on authenticated route.
        """
        res = self.client.get('/secret', headers={'auth-token': 'token'})
        self.assertEqual(res.status_code, 403)

    def test_get_authenticated_route_with_expired_token(self):
        """
        Validates that an expired token doesn't work on authenticated route.
        """
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NTUwNzQ3MjR9\
                .LTm9mFZXQTzqpYKgOb3C10Zxu50bfom-fX6OsHmd-a4'
        res = self.client.get('/secret', headers={'auth-token': token})
        self.assertEqual(res.status_code, 403)
