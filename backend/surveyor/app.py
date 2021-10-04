import dataclasses
import os

from flask import Flask, json
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException

import auth
import database
import survey
import survey_submission


class _EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)  # convert dataclass instances to dict
        return super().default(o)


is_development_environment = os.environ.get('ENV', 'prod') == 'dev'


def _handle_exception(e: HTTPException):
    """Return JSON instead of HTML for HTTP errors."""
    # if isinstance(e, HTTPException):
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


def create_app():
    app = Flask(__name__)
    app.config.update(dict(
        DEBUG=is_development_environment,
        SECRET_KEY='secret_xxx',
    ))
    app.json_encoder = _EnhancedJSONEncoder
    app.register_error_handler(HTTPException, _handle_exception)

    JWTManager(app)
    database.init_app(app)

    # register views
    auth.init_app(app)
    survey.init_app(app)
    survey_submission.init_app(app)

    return app


if __name__ == '__main__':
    # in development, we will expose the API to be accessible on from any IP of the host
    host = '0.0.0.0' if is_development_environment else 'localhost'
    app = create_app()
    app.run(host=host, debug=is_development_environment, )
