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

engine = create_engine('sqlite:///:memory:', echo=True)
session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)
Model = declarative_base()


class User(Model):
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
        expiration = datetime.utcnow() + timedelta(minutes=20)
        payload = {
            'exp': expiration,
            'user': self.id
        }
        return jwt.encode(payload, secret)

    def authenticate(self, password):
        if checkpw(password.encode('utf-8'), self.hashed_password):
            return self.generate_token()

