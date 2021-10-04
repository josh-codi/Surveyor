import os
from typing import Union

from flask import Flask, json
from flask.helpers import make_response
from flask_jwt_extended import JWTManager

from werkzeug.exceptions import HTTPException
import logging
import auth
from app import app

is_development_mode = os.environ.get('ENV', 'prod') == 'dev'


if __name__ == '__main__':
    # in development, we will expose the API to be accessible on from any IP of the host
    host = '0.0.0.0' if is_development_mode else 'localhost'
    app.run(host=host, debug=is_development_mode, )
