
from app.db.data import User, Auth
from app.engine.operation import *


# Modification


def create_user(email, pw):
    """
    Creates a new user, provided one does not already exist
    
    :param email: The email address the user wishes to use
    :param pw: The password the user wishes to use
    :return: True if the user was created successfully. False otherwise
    """
    pass


def delete_user(email, pw):
    """
    Deletes an existing user from the database
    
    :param email: The user's email
    :param pw: The user's password
    :return: A success response detailing if the user was found. Otherwise a warning response
    """
    pass


def log_in(email, pw):
    """
    Begins an authentication session if the provided credentials are matched in the system
    
    :param email: The user's email address
    :param pw: The user's password
    :return: Response containing the user's authentication key if the correct credentials are provided. Otherwise a
    warning response
    """
    pass


def authenticate(auth_key):
    """
    Refreshes a user's authentication using a previously provided authentication key. The authentication must
    not have expired in order to be refreshed
    
    :param auth_key: The user's authentication key
    :return: Success response determining if the authentication was successful or not
    """
    pass


def log_out(auth_key):
    """
    Terminates a user's authentication session immediately
    
    :param auth_key: The user's authentication key
    :return: Success response determining if the user was successfully logged out
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
