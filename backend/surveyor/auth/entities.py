from pony.orm.core import Required, Set
from database import BaseEntity


class User(BaseEntity):
    username: str = Required(str, unique=True)
    password: str = Required(str)
    name: str = Required(str, autostrip=True)
    # a list of surveys created by this user(survey admin)
    # surveys = Set('Survey', lazy=True)
