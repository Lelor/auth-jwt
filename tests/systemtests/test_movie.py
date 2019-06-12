"""User actions system tests module."""
from unittest import TestCase
from datetime import datetime

from api import create_app
from api.models import engine, Base, session, Movie, MovieGenre
from api.modules.movie import save_object


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

    def test_registrate_movie_with_invalid_genre_id(self):
        """Validates movie registratoin when the route receives valid data."""
        data = {
            'name': 'testmovie',
            'release_date': datetime.utcnow().isoformat(),
            'director': 'test',
            'genre_id': 2,
            'picture': 'abc'
        }
        res = self.client.post('/movie', json=data)
        query = session.query(Movie).all()
        self.assertEqual(res.status_code, 400)
        self.assertEqual(len(query), 0)

    def test_registrate_movie_with_valid_data(self):
        """Validates movie registratoin when the route receives valid data."""
        save_object(MovieGenre(text='test'))
        data = {
            'name': 'testmovie',
            'release_date': datetime.utcnow().isoformat(),
            'director': 'test',
            'genre_id': 1,
            'picture': 'abc'
        }
        res = self.client.post('/movie', json=data)
        query = session.query(Movie).all()
        self.assertEqual(res.status_code, 201)
        self.assertEqual(len(query), 1)

        res = self.client.get('/list_movies')

    def test_registrate_movie_genre_with_valid_data(self):
        data = {'text': 'test'}
        res = self.client.post('/movie_genre', json=data)
        query = session.query(MovieGenre).all()
        self.assertEqual(res.status_code, 201)
        self.assertEqual(len(query), 1)
