import functools

from flask import abort, g
from flask_jwt_extended import jwt_required


@jwt_required
def login_required(view):
    """View decorator that throws an UnauthorizedException
    if there is currently no authenticated user """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            abort(401)

        return view(**kwargs)

    return wrapped_view
