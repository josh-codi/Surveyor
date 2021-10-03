import os
from typing import Union

from flask import Flask, json
from flask.helpers import make_response
from flask_jwt_extended import JWTManager

from pony.flask import Pony
from werkzeug.exceptions import HTTPException

from database import db
import auth

is_development_mode = os.environ.get('ENV', 'prod') == 'dev'

app = Flask(__name__)
app.config.update(dict(
    DEBUG=is_development_mode,
    SECRET_KEY='secret_xxx',
    PONY={
        'provider': 'sqlite',
        'filename': 'surveyor_db.sqlite',
        'create_db': True
    }
))
jwt = JWTManager(app)


@app.errorhandler(Exception)
def handle_exception(e: Union[HTTPException, Exception]):
    """Return JSON instead of HTML for HTTP errors."""
    if isinstance(e, HTTPException):
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

    response = make_response(
        json.jsonify({'error': 'Internal Server Error'})
    )
    response.status_code = 500
    return response


Pony(app)

# register views
auth.init_app(app)

# establish a connection pool (managed by Pony) to the database
db.bind(**app.config['PONY'])
db.generate_mapping(create_tables=True)


if __name__ == '__main__':
    # in development, we will expose the API to be accessible on from any IP of the host
    host = '0.0.0.0' if is_development_mode else 'localhost'
    app.run(host=host, debug=is_development_mode, )
