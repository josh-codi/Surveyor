import functools

from flask import abort, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from typing import Union
import logging
from .service import User


def login_required(view):
    """View decorator that throws an UnauthorizedException
    if there is currently no authenticated user """

    @functools.wraps(view)
    @jwt_required()  # <-- ensures that the Authorization header contains a valid JWT
    def wrapped_view(*args, **kwargs):
        # load user instance into G object
        try:
            # 'user_data' is the object passed as identity when creating access_token
            user_data: Union[str, None] = get_jwt_identity()
        except Exception as error:
            logging.error('Failed to get JWT identity')
            logging.error(error)
            user_data = None
        setattr(g, 'user', None if user_data is None else User(**user_data))

        if getattr(g, 'user', None) is None:
            abort(401, 'Not authenticated. Login is required')

        return view(*args, **kwargs)

    return wrapped_view
