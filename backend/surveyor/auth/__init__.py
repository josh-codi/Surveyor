from flask import g
from flask.app import Flask

from auth.service import User

from .views import AuthView


def _clear_user_on_request_end(*args, **kwargs):
    setattr(g, 'user', None)


def init_app(app: Flask):
    app.teardown_request(_clear_user_on_request_end)
    AuthView.register(app, route_base='/auth')


def get_current_user() -> User:
    return g.user
