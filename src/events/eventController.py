from bson import ObjectId
from flask import Blueprint, request, session, Response

from .eventModel import EventSchema, EventCoverSchema
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
from .eventService import EventService
from .eventDAO import EventDAO
from marshmallow import ValidationError
from pymongo import errors
from src.common.commonService import upload_file_to_gcs, download_from_gcs, upload_event_cover_image
import os

event_bp = Blueprint("events", __name__, url_prefix="/event")
eventSchema = EventSchema()
eventDAO = EventDAO()
eventService = EventService()
eventCoverSchema = EventCoverSchema()



@event_bp.get("/")
def get_events():
    try:
        events = eventDAO.find_all()
        return good_response(events)
    except Exception as e:
        print(e)
        return server_error()
    

@event_bp.post("/cover/upload/<id>")
def upload_events(id:str):
# Check if the request contains a file
    found_event = eventDAO.find_by_id(id)
    if not found_event:
        return bad_request("Event not found!")
    
    if 'file' not in request.files:
        return bad_response("File not found!")

    file = request.files['file']

    # Check if a file is selected
    if file.filename == '':
        return bad_response("File not selected!")

    # Upload the file to Google Cloud Storage
    # try:
    public_url = upload_event_cover_image(file, found_event)
    return good_response({"cover_url": os.getenv("SERVER_URL")+"event/cover/"+public_url})
    # except Exception as e:
    #     return server_error()


@event_bp.post("/create")
@adminProtected
def create_event():
    try:
        data = eventSchema.load(request.get_json())
        event = eventService.create_event(data)
        if event == None:
            return bad_response("Event Exist!")
        return good_response(event)

    except Exception as e:
        print(e)
        if isinstance(e, ValidationError):
            return bad_response(e.messages)
        elif isinstance(e, errors.DuplicateKeyError):
            return bad_response("Something went wrong!")
        return server_error()
    
    
@event_bp.post("/cover/<id>")
@adminProtected
def set_cover_url(id:str):
    try:
        data = eventCoverSchema.load(request.get_json())
        event_found = eventDAO.find_by_id(id)
        
        if event_found:
            eventDAO.change_cover_image(event_found["_id"], data["cover_url"])
            return good_response({**event_found, "cover_url": data["cover_url"]})
        return bad_response("Something went wrong with the image data or event data")

    except Exception as e:
        print(e)
        if isinstance(e, ValidationError):
            return bad_response(e.messages)
        elif isinstance(e, errors.DuplicateKeyError):
            return bad_response("Something went wrong!")
        return server_error()
    

@event_bp.get("/cover/<image>")
def get_event_cover(image : str):
    image_data, content_type = download_from_gcs(image)    
    return Response(image_data, content_type=content_type)