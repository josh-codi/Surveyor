from typing import Union

from flask import g
from flask.app import Flask
from flask_jwt_extended import get_jwt_identity

from auth.service import AuthService
from .views import AuthView
from database import get_db


def _load_logged_in_user_on_request_start():
    """
    Called at the start of each request, to fetch the current user into memory
    """
    try:
        user_id: Union[str, None] = get_jwt_identity()
    except Exception as error:
        user_id = None

    if user_id is None:
        setattr(g, 'user', None)
    else:
        db = get_db()
        user = AuthService().get_user_by_id(db, user_id)
        setattr(g, 'user', user)


def _clear_user_on_request_end(*args, **kwargs):
    setattr(g, 'user', None)


def init_app(app: Flask):
    app.before_request(_load_logged_in_user_on_request_start)
    app.teardown_request(_clear_user_on_request_end)
    AuthView.register(app, route_base='/auth')
