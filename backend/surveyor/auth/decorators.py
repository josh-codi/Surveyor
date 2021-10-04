import functools

from flask import abort, g
from flask_jwt_extended import jwt_required


def login_required(view):
    """View decorator that throws an UnauthorizedException
    if there is currently no authenticated user """

    @functools.wraps(view)
    @jwt_required()
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            abort(401, 'Not authenticated. Login is required')

        return view(*args, **kwargs)

    return wrapped_view
