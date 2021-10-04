from dataclasses import dataclass
from datetime import datetime, timedelta
from sqlite3.dbapi2 import Connection, IntegrityError, Row
from typing import Optional, Tuple, Union

from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash


@dataclass
class User:
    id: int
    name: str
    username: str
    created_at: datetime = None
    updated_at: datetime = None
    password: str = '<redacted-for-security-reasons>'


class AuthService(object):

    @classmethod
    def create_root_user_if_not_exists(cls, db: Connection) -> User:
        try:
            root_user = cls.register_user(
                db, username='master', password='keypass', name='Attaa Adwoa')
        except IntegrityError:
            root_user = cls._get_user_by_username(
                db, username='master', hide_password=True)
        return root_user

    @classmethod
    def register_user(cls, db: Connection, username: str, password: str, name: str) -> User:
        password_hash = generate_password_hash(password)
        user_id: int = db.execute(
            'INSERT INTO user (username, password, name) VALUES (?, ?, ?)',
            (username, password_hash, name)
        ).lastrowid
        return AuthService.get_user_by_id(db, user_id)

    @classmethod
    def verify_user(cls, db: Connection, username: str, password: str) -> Tuple[bool, Union[User, None]]:
        user = AuthService._get_user_by_username(
            db, username, hide_password=False)
        if user is None:
            return False, None
        if not check_password_hash(user.password, password):
            return False, None

        # hide password now - we're done using it
        user.password = '<redacted-for-security-reasons>'
        return True, user

    @classmethod
    def _get_user_by_username(cls, db: Connection, username: str, hide_password=True) -> Optional[User]:
        user_data: Union[Row, None] = db.execute(
            'SELECT * FROM user WHERE username=? LIMIT 1',
            (username,)
        ).fetchone()
        if user_data is None:
            return None

        return User(**{
            **user_data,
            'password': '<redacted-for-security-reasons>' if hide_password else user_data['password']
        })

    @classmethod
    def get_user_by_id(cls, db: Connection, user_id: int):
        user_data = db.execute(
            '''
            SELECT id, name, username, created_at, updated_at
            FROM user WHERE id=? LIMIT 1
            ''',
            (user_id,)
        ).fetchone()
        if user_data is None:
            return None
        return User(**user_data)

    @classmethod
    def get_access_token_for_user(cls, user: User) -> str:
        return create_access_token(identity=user, expires_delta=timedelta(days=1))
