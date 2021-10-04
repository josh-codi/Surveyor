import sqlite3
from sqlite3.dbapi2 import Connection
from typing import final
from flask import g, Flask
import os
import functools
import logging
import traceback


DATABASE = f'{os.path.dirname(os.path.abspath(__file__))}/surveyor_db.sqlite'


def autocommit_db_changes(view):
    """ View decorator that automatically commits/persists database changes to disk """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        db = get_db()
        response = view(**kwargs)
        db.commit()
        return response
    return wrapped_view


def get_db() -> Connection:
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        logging.info('Opened database connection')
        db.row_factory = sqlite3.Row
    return db


def _close_database_connection(exception=None):
    db = getattr(g, '_database', None)
    if db is not None:
        logging.info('Closed database connection')
        db.close()


def _init_db(app: Flask):
    with app.app_context():
        db = get_db()
        try:
            with app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()
        except Exception as error:
            logging.error('Failed to initialise database')
            traceback.print_exception()
        else:
            logging.info('Initialized database')
        finally:
            _close_database_connection()


def init_app(app: Flask):
    _init_db(app)

    # close any db connection when ending request
    app.teardown_appcontext(_close_database_connection)
