
from app.db.data import User, Auth
from app.engine.operation import *

from datetime import datetime, timedelta

expire_minutes=30

# Modification


def create_user(email, pw):
    """
    Creates a new user, provided one does not already exist
    
    :param email: The email address the user wishes to use
    :param pw: The password the user wishes to use
    :return: True if the user was created successfully. False otherwise
    """
    user = User.objects(email=email, pw=pw).first()

    if user is None:
        user = User(email=email, pw=pw)
        user.save()
        return True
    else:
        return False


def delete_user(email, pw):
    """
    Deletes an existing user from the database
    
    :param email: The user's email
    :param pw: The user's password
    :return: True if the user was found and deleted. False otherwise
    """
    user = User.objects(email=email, pw=pw).first()

    if user is not None:
        user.delete()
        return True
    else:
        return False


def authenticate(email, pw):
    """
    Begins an authentication session if the provided credentials are matched in the system
    
    :param email: The user's email address
    :param pw: The user's password
    :return: The user's authentication key if the log in was successful. None otherwise
    """
    user = User.objects(email=email, pw=pw).first()

    if user is None:
        return False

    else:
        key = get_auth_key(email, True)

        if Auth.objects(key=key).count() == 0:
            auth = Auth(key=key, user=user, expire_time = datetime.now() + timedelta(minutes=expire_minutes))
            auth.save()

        return key


def validate_auth(auth_key, email):
    """
    Refreshes a user's authentication using a previously provided authentication key. The authentication must
    not have expired in order to be refreshed
    
    :param auth_key: The user's authentication key
    :param email: The user's email
    :return: Success response determining if the authentication was successful or not
    """
    user = User.objects(email=email).first()

    if user is not None:
        auth = Auth.objects(key=auth_key, user=user).first()

        if auth is not None and auth.expire_time >= datetime.now():
            auth.expire_time = datetime.now() + timedelta(minutes=expire_minutes)
            auth.save()
            return True
        else:
            return False
    else:
        return False


def clear_auth(auth_key):
    """
    Terminates a user's authentication session immediately
    
    :param auth_key: The user's authentication key
    :return: Success response determining if the user was successfully logged out
    """
    pass


def log_out(email):
    """
    Eliminates a user's authentication data using their email address rather than their authentication key
    
    :param email: The user's email address
    :return: True if the authentication was found and cleared successfully. False otherwise
    """
    pass

# Queries


def user_exists(email):
    """
    Query which determines if a user exists in the system
    
    :param email: The user's email address
    :return: True if the user exists, or false otherwise
    """
    return False


def get_auth_key(email, generate):
    """
    Query used to get the user's authentication key
    
    :param email: The user's email address
    :param generate: If true, a new key will be generated if one does not exist
    :return: The user's authentication key if the user has one or one was generated, otherwise None
    """
    return None
