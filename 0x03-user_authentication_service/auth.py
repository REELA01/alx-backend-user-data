#!/usr/bin/env python3
"""definie _hash_password function"""
import bcrypt
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from typing import (
    TypeVar,
    Union
)

from db import DB
from user import User

U = TypeVar(User)


def _hash_password(password: str) -> bytes:
    """hashes a password string and returns it in bytes func"""
    paswd = password.encode('utf-8')
    return bcrypt.hashpw(paswd, bcrypt.gensalt())


def _generate_uuid() -> str:
    """generate a uuid and return its string representation"""
    return str(uuid4())


class Auth:
    """auth class to interact with the authentication database"""

    def __init__(self) -> None:
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a new user and return a user object"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password)
            usr = self._db.add_user(email, hashed)
            return usr
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """validate a user's login credential"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        user_password = user.hashed_password
        passwd = password.encode("utf-8")
        return bcrypt.checkpw(passwd, user_password)

    def create_session(self, email: str) -> Union[None, str]:
        """create a session_id for an existing user and update the user's"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[None, U]:
        """takes a session_id and returns the corresponding user"""
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """take a user_id and destroy that user's session"""
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """generates uuid for a user identified by the given email"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """updates a user's password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()

        hashed = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed, reset_token=None)
