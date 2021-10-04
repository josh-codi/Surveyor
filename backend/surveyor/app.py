import os

from flask import Flask, json
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException
import auth
import survey
import survey_submission
from database import init_app
import dataclasses


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)  # convert dataclass instances to dict
        return super().default(o)


is_development_mode = os.environ.get('ENV', 'prod') == 'dev'

app = Flask(__name__)
app.config.update(dict(
    DEBUG=is_development_mode,
    SECRET_KEY='secret_xxx',
))
app.json_encoder = EnhancedJSONEncoder


@app.errorhandler(HTTPException)
def handle_exception(e: HTTPException):
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


jwt = JWTManager(app)
init_app(app)

# register views
auth.init_app(app)
survey.init_app(app)
survey_submission.init_app(app)
