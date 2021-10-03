from typing import Tuple, Union
from .entities import User
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from pony.orm.core import db_session, select, commit
from flask_jwt_extended import create_access_token


class AuthService(object):

    @db_session
    def register_user(self, username: str, password: str, name: str):
        password_hash = generate_password_hash(password)
        user = User(username=username, password=password_hash, name=name)
        commit()  # save user and throw errors (eg: username unique constraint violation) if any
        return user

    @db_session
    def verify_user(self, username: str, password: str) -> Tuple[bool, Union[User, None]]:
        query = select(u for u in User if u.username == username)
        user: Union[User, None] = query.first()
        if user is None:
            return False, None
        if not check_password_hash(user.password, password):
            return False, None
        return True, user

    def get_access_token_for_user(self, user: User) -> str:
        return create_access_token(identity=user.username)
