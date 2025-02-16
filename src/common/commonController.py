from bson import ObjectId
from flask import Blueprint, request, session

from .commonModel import EventSchema
from utils.response import (
    bad_response,
    good_response,
    server_error,
    not_found,
    unauthorized,
)


from utils.token import gen_token, get_user_from_token
from middlewares.auth import adminProtected
import bcrypt
import uuid
from .commonService import EventService
from .commonDAO import EventDAO
from marshmallow import ValidationError
from pymongo import errors


common_bp = Blueprint("common", __name__, url_prefix="/")
commonSchema = EventSchema()
commonDAO = EventDAO()
commonService = EventService()



@common_bp.get("/")
def get_commons():
    try:
        commons = commonDAO.find_all()
        return good_response(commons)
    except Exception as e:
        print(e)
        return server_error()


@common_bp.post("/create")
@adminProtected
def create_common():
    try:
        data = commonSchema.load(request.get_json())
        common = commonService.create_common(data)
        if common == None:
            return bad_response("Event Exist!")
        return good_response(common)

    except Exception as e:
        print(e)
        if isinstance(e, ValidationError):
            return bad_response(e.messages)
        elif isinstance(e, errors.DuplicateKeyError):
            return bad_response("Something went wrong!")
        return server_error()
    
    
