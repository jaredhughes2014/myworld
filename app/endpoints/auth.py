
import app.db.functions.auth as db
from app.engine.operation import *


def create_user(email, pw):
    """
    Endpoint used to handle the task of creating a new user
    
    :param email: The provided email address
    :param pw: The provided password
    """
    exists = yield Execute(db.user_exists, email)

    if exists:
        yield Respond.warning_response('Account already exists for {}'.format(email))
    else:
        yield Execute(db.create_user, email, pw)
        yield Respond.success_response(True)


def delete_user(email, pw):
    """
    Endpoint used to handle the task of deleting a user
    
    :param email: The provided email address
    :param pw: The provided password
    """
    yield None


def authenticate(email, pw):
    """
    Endpoint used to handle the task of logging a user in
    
    :param email: The provided email address
    :param pw: The provided password
    """
    yield None


def validate_auth(key, email):
    """
    Endpoint used to handle the task of authenticating a user
    
    :param key: The provided authentication key
    :param email: The provided email address
    """
    yield None


def log_out(key):
    """
    Endpoint used to handle the task of logging a user out
    
    :param key: The provided authentication key
    """
    yield None
