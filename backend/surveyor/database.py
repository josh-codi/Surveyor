from datetime import datetime
from enum import Enum
import logging
from typing import Union
import uuid
from pony.orm.core import Database, PrimaryKey, Required
from logging import debug

''' Global database singleton used in the entire application.'''
db = Database()


@db.on_connect(provider='sqlite')
def on_database_connected(db: Database, connection):
    debug("Connected to database with provider '%s'", db.provider_name)


class BaseEntity(db.Entity):
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, default=datetime.utcnow)
    updated_at = Required(datetime, default=datetime.utcnow)
