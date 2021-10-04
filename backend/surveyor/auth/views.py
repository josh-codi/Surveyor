from sqlite3.dbapi2 import IntegrityError
from flask.json import jsonify
from flask_classy import FlaskView, route
from flask import request, abort
from auth.decorators import login_required
from database import autocommit_db_changes

from database import get_db

from .service import AuthService


class AuthView(FlaskView):
    def __init__(self) -> None:
        super().__init__()
        self.auth_service = AuthService()

    decorators = [autocommit_db_changes]

    @route('/sign-in', methods=["POST"])
    def sign_in(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        is_verified, user = self.auth_service.verify_user(
            get_db(), username, password)
        if not is_verified:
            abort(401)

        return jsonify({
            'access_token': self.auth_service.get_access_token_for_user(user),
            'user': user
        }), 200

    @route('/sign-up', methods=["POST"])
    def sign_up(self):
        user_info: dict = request.json
        try:
            user = self.auth_service.register_user(get_db(), ** user_info)
        except IntegrityError:
            abort(400, 'username is not available')
        return jsonify({
            'access_token': self.auth_service.get_access_token_for_user(user),
            'user': user
        }), 201

    @login_required
    @route('/change-password', methods=['POST'])
    def change_password(self):
        abort(500, 'Not implemented')
