
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
    yield Execute(db.log_out, email)
    deleted = yield Execute(db.delete_user, email, pw)

    if deleted:
        yield Respond.success_response(True)
    else:
        yield Respond.error_response('No user with email {} exists'.format(email))


def authenticate(email, pw):
    """
    Endpoint used to handle the task of logging a user in
    
    :param email: The provided email address
    :param pw: The provided password
    """
    exists = yield Execute(db.user_exists, email)

    if exists:
        auth_key = yield Execute(db.get_auth_key, email, True)
        valid = yield Execute(db.validate_auth, auth_key, email)

        if valid:
            yield Respond(key=auth_key)

    else:
        yield Respond.error_response("Invalid credentials")


def validate_auth(key, email):
    """
    Endpoint used to confirm a user is still authenticated and is
    
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
