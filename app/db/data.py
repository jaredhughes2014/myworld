
from mongoengine import *


class User(Document):
    """
    Users contain data about the people who use this software
    """
    pass


class Auth(Document):
    """
    Auth contains metadata about user's authentication. This is used to maintain timed sessions
    """
    pass
