
from mongoengine import *


class User(Document):
    """
    Users contain data about the people who use this software
    """

    email = EmailField(required=True, primary_key=True)

    pw = StringField(required=True)


class Auth(Document):
    """
    Auth contains metadata about user's authentication. This is used to maintain timed sessions
    """
    key = StringField(required=True, primary_key=True)

    user = ReferenceField(User(), required=True)
