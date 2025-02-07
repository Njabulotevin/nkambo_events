from bson import ObjectId
from flask import Blueprint, request, session

from .eventModel import EventSchema
from utils.response import (
    bad_response,
    good_response,
    server_error,
    not_found,
    unauthorized,
)


from utils.token import gen_token, get_user_from_token
from middlewares.auth import instructorProtected, protectedRoute, studentProtected
import bcrypt
import uuid
from .eventService import is_valid_user, get_user
from .eventDAO import EventDAO
from marshmallow import ValidationError
from pymongo import errors


event_bp = Blueprint("events", __name__, url_prefix="/event")
eventSchema = EventSchema()
eventDAO = EventDAO()



@event_bp.get("/")
def get_events():
    try:
        events = eventDAO.find_all()
        return good_response(events)
    except Exception as e:
        print(e)
        return server_error()


@event_bp.post("/create")
# @instructorProtected
def create_event():
    try:
        data = eventSchema.load(request.get_json())
        event = eventDAO.save_event(data)
        return good_response(event)

    except Exception as e:
        print(e)
        if isinstance(e, ValidationError):
            return bad_response(e.messages)
        elif isinstance(e, errors.DuplicateKeyError):
            return bad_response("Something went wrong!")
        return server_error()

