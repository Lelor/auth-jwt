from flask import current_app
from sqlalchemy.exc import IntegrityError

from api.models import Movie, MovieGenre
from api.serializer.user import MovieSchema


def save_object(movie):
    """
    Receives the movie data and saves it on the database.

    Args:
        movie: SQLAlchemy object that represents the movie entity

    Returns:
        on success: registered movie object.
        on failure: None
    """
    try:
        current_app.session.add(movie)
        current_app.session.commit()
        return movie
    except IntegrityError:
        current_app.session.rollback()


def get_genre_by_id(genre_id):
    return current_app.session.query(MovieGenre).filter_by(id=genre_id).first()


def list_all_movies():
    movies = current_app.session.query(Movie).all()
    return MovieSchema(many=True).jsonify(movies)
