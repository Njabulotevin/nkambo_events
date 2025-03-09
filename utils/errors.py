from marshmallow import ValidationError
from pymongo import errors

from utils.response import bad_response, server_error


def exception_with_validation(e):
    print(e)
    if isinstance(e, ValidationError):
        return bad_response(e.messages)
    elif isinstance(e, errors.DuplicateKeyError):
        return bad_response("Something went wrong!")
    return server_error()
