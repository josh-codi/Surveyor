import dataclasses
from datetime import timedelta
from sqlite3.dbapi2 import Connection, IntegrityError, Row
from typing import Optional, Tuple, Union
from werkzeug.exceptions import HTTPException
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    username: str


class AuthService(object):

    @staticmethod
    def register_user(db: Connection, username: str, password: str, name: str) -> User:
        password_hash = generate_password_hash(password)
        user_id: int = db.execute(
            'INSERT INTO user (username, password, name) VALUES (?, ?, ?)',
            (username, password_hash, name)
        ).lastrowid
        return User(id=user_id, username=username, name=name)

    @staticmethod
    def verify_user(db: Connection, username: str, password: str) -> Tuple[bool, Union[User, None]]:
        user_data: Union[Row, None] = db.execute(
            'SELECT * FROM user WHERE username=? LIMIT 1',
            (username,)
        ).fetchone()
        if user_data is None:
            return False, None
        if not check_password_hash(user_data['password'], password):
            return False, None
        allowed_fields = set(f.name for f in dataclasses.fields(User))
        return True, User(**{k: user_data[k] for k in user_data.keys() if k in allowed_fields})

    @staticmethod
    def get_user_by_id(db: Connection, user_id: int):
        user_data = db.execute(
            f'SELECT id, name, username FROM user WHERE id=? LIMIT 1', (
                user_id,)
        ).fetchone()
        if user_data is None:
            return None
        return User(**user_data)

    def get_access_token_for_user(self, user: User) -> str:
        return create_access_token(identity=user, expires_delta=timedelta(days=1))
