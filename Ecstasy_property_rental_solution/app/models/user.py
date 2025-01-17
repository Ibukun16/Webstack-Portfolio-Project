#!/usr/bin/env python3
"""Module that handles the User class"""
import jwt
import models
import sqlalchemy as sa
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from hashlib import md5
from werkzeug.security import check_password_hash
from datetime import datetime, timezone, timedelta


class User(BaseModel, Base, UserMixin):
    """Function that represent the user class"""
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False, unique=True)
        username = Column(String(128), nullable=False, unique=True)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email: ""
        username = ""
        password = ""
       first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """Initializing the user class"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """Set password encryption with md5"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().setattr__(name, value)
    
    def check_password(self, password):
        return check_password_hash(self.__setattr__, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
                {'reset_password': self.id, 'exp': time() + expires_in},
                current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except Exception:
            return
        return storage.session.get(User, id)

    def add_notification(self, name, data):
        storage.session.execute(self.notifications.delete().where
                                Notification.name == name))
        new = Notification(name=name, payload_json=json.dumps(data), user=self)
        storage.session.add(new)
        return new

    def unread_message_count(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        query = sa.select(Message).where(Message.recipient == self,
                                         Message.timestamp > last_read_time)
        return storage.session.scalar(sa.select(sa.func.count()).select_from(
            query.subquery()))

    def get_token(self, expires_in=3600):
        now = datetime.now(timezone.utc)
        if self.token and self.token_expiration.replace(
                tzinfo=timezone.utc) > now + timedelta(seconds=60):
            return self.token
        self.token = secrets.token_hex(16)
        self.token_expiration = now + timedelta(seconds=expires_in)
        storage.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.now(timezone.utc) - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = storage.session.scalar(sa.select(User).where(User.token == token))
        if user is None or user.token_expiration.replace(
                tzinfo=timezone.utc) < datetime.now(timezone.utc):
            return None
        return user


    @login.user_loader
    def load_user(id):
        return storage.session.get(User, int(id))
