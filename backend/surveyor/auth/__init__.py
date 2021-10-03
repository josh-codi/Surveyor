from typing import Union

from flask import g
from flask.app import Flask
from flask.json import jsonify
from flask_jwt_extended import get_jwt_identity
from pony.orm.core import db_session, select
from .entities import User
from werkzeug.exceptions import HTTPException
import logging
from .views import AuthView


@db_session
def _load_logged_in_user_on_request_start():
    """
    Called at the start of each request, to fetch the current user into memory
    """
    try:
        user_id: Union[str, None] = get_jwt_identity()
    except Exception as error:
        logging.error(error)
        user_id = None

    if user_id is None:
        setattr(g, 'user', None)
    else:
        user = select(u for u in User if u.id == user_id).first()
        setattr(g, 'user', user)


def init_app(app: Flask):
    app.before_request(_load_logged_in_user_on_request_start)
    AuthView.register(app, route_base='/auth')
