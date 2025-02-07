from flask import session
from utils.token import is_admin, is_allowed_role, is_instructor, is_student, is_valid_token
from utils.response import unauthorized
from functools import wraps


def protectedRoute(fn):
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        print("Is there a token? ", "token" in session)
        if "token" in session:
            token = session["token"]
            print("is valid token: ", is_valid_token(token))
            if not token or not is_valid_token(token):
                return unauthorized()
        else:
            return unauthorized()
        return fn(*args, **kwargs)

    return decorated_function


def instructorProtected(fn):
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        if "token" in session:
            token = session["token"]
            if not token or not is_instructor(token):
                return unauthorized()
        else:
            return unauthorized()
        return fn(*args, **kwargs)
    return decorated_function


def adminProtected(fn):
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        if "token" in session:
            token = session["token"]
            if not token or not is_admin(token):
                return unauthorized()
        else:
            return unauthorized()
        return fn(*args, **kwargs)
    return decorated_function


def studentProtected(fn):
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        if "token" in session:
            token = session["token"]
            if not token or not is_student(token):
                return unauthorized()
        else:
            return unauthorized()
        return fn(*args, **kwargs)
    return decorated_function


def check_role_in_token(role):
    if "token" in session:
        token = session["token"]
        print("is valid token: ", is_allowed_role(token, role))
        if not token or not is_valid_token(token):
            return unauthorized()
    else:
        return unauthorized()
