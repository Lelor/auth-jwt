from datetime import datetime, timedelta

import jwt
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy import (Column,
                        DateTime,
                        Integer,
                        String,
                        create_engine)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

secret = 'super_secret'

engine = create_engine('sqlite:///:memory:', echo=False)
session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)
Base = declarative_base()


class User(Base):
    """User table."""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = hashpw(password.encode('utf-8'), gensalt(8))

    def generate_token(self):
        """
        Generates the JWT token with a 20min expiration and the user id.
        """
        expiration = datetime.utcnow() + timedelta(minutes=20)
        payload = {
            'exp': expiration,
            'user': self.id
        }
        return jwt.encode(payload, secret).decode('utf-8')

    def authenticate(self, password):
        """
        Authenticates the user by checking the given password.

        Args:
            str password: password inputed by the user.
        
        Returns:
            on success: JWT token with a 20min expiration and the user id.
            on failure: None
        """
        if checkpw(password.encode('utf-8'), self.password_hash):
            return self.generate_token()
