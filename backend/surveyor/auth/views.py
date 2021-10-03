from flask.helpers import make_response
from flask.json import jsonify
from flask_classy import FlaskView, route
from flask import request, abort

from .service import AuthService


class AuthView(FlaskView):
    def __init__(self) -> None:
        super().__init__()
        self.auth_service = AuthService()

    @route('/sign-in', methods=["POST"])
    def sign_in(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        is_verified, user = self.auth_service.verify_user(username, password)
        if not is_verified:
            abort(401)

        return jsonify({
            'access_token': self.auth_service.get_access_token_for_user(user),
            'user': user.to_dict(exclude=('password',))
        }), 200

    @route('/sign-up', methods=["POST"])
    def sign_up(self):
        user_info: dict = request.json
        user = self.auth_service.register_user(**user_info)
        return jsonify(user.to_dict(exclude=('password',))), 201
