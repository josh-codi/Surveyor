import sqlite3
from sqlite3.dbapi2 import Connection, Cursor
from flask import g, Flask
import os
import functools
import logging
import traceback

from auth.service import AuthService


DATABASE = f'{os.path.dirname(os.path.abspath(__file__))}/surveyor_db.sqlite'


def autocommit_db_changes(view):
    """ View decorator that automatically commits/persists database changes to disk """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        db = get_db()
        db.rollback()
        response = view(**kwargs)
        db.commit()
        return response
    return wrapped_view


def _dict_factory(cursor: Cursor, row: tuple):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db() -> Connection:
    db = getattr(g, '_database', None)
    if db is None:
        # open a connection to the database
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = _dict_factory  # rows will be represented as regular python dicts
    return db


def _close_database_connection(exception=None):
    # existing database connection if any, else None
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
    setattr(g, '_database', None)  # remove connection object from memory


def _init_db(app: Flask):
    with app.app_context():
        db = get_db()
        try:
            with app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            AuthService.create_root_user_if_not_exists(db)
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
