from bson import ObjectId
from flask import Blueprint, request, session, Response

from utils.errors import exception_with_validation
from .eventModel import EventSchema, EventCoverSchema, NewGuestSchema, GetEeventGuestSchema
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
from src.common.commonService import upload_to_supabase, get_file_from_supabase
import os
from mimetypes import guess_type

from src.guests.guestDAO import GuestDAO

event_bp = Blueprint("events", __name__, url_prefix="/event")
eventSchema = EventSchema()
eventDAO = EventDAO()
eventService = EventService()
eventCoverSchema = EventCoverSchema()
newGuestSchema = NewGuestSchema()
guestDAO = GuestDAO()
getEeventGuestSchema = GetEeventGuestSchema()

@event_bp.get("/")
def get_events():
    """
    Get a list of events
    ---

    responses:
      200:
        description: List of events
        examples:
          application/json: {"status": 200, "data" : []}
    """
    try:
        events = eventDAO.find_all()
        return good_response(events)
    except Exception as e:
        print(e)
        return server_error()


@event_bp.get("/<id>")
def get_event_by_id(id: str):
    """
    Get event by ID
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The unique identifier of the event
    responses:
      200:
        description: Event found successfully
        schema:
          type: object
          properties:
            id:
              type: string
              description: The unique identifier of the event
            name:
              type: string
              description: The name of the event
            description:
              type: string
              description: A short description of the event
            location:
              type: string
              description: The location of the event
            start_date:
              type: string
              format: date
              description: The start date of the event
            end_date:
              type: string
              format: date
              description: The end date of the event
            start_time:
              type: string
              description: The start time of the event
            end_time:
              type: string
              description: The end time of the event
            ticket_price:
              type: number
              format: float
              description: The price of one ticket for the event
            ticket_quantity:
              type: integer
              description: The total number of tickets available for the event
        examples:
          application/json: {
            "id": "1",
            "name": "test event5",
            "description": "just an event",
            "location": "123 address",
            "start_date": "12 June 2024",
            "end_date": "12 June 2024",
            "start_time": "20:00",
            "end_time": "20:00",
            "ticket_price": 300,
            "ticket_quantity": 3
          }
      404:
        description: Event not found
      500:
        description: Internal server error
    """
    try:
        event = eventDAO.find_by_id(id)
        if not event:
            return not_found()
        return good_response(event)
    except Exception as e:
        print(e)
        return server_error()


@event_bp.post("/create")
@adminProtected
def create_event():
    """
    Create a new event
    ---
    parameters:
      - in: body
        name: event
        description: Event data to be created
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: The name of the event
            description:
              type: string
              description: A brief description of the event
            location:
              type: string
              description: The location where the event is held
            start_date:
              type: string
              format: date
              description: The start date of the event
            end_date:
              type: string
              format: date
              description: The end date of the event
            start_time:
              type: string
              format: time
              description: The start time of the event
            end_time:
              type: string
              format: time
              description: The end time of the event
            ticket_price:
              type: integer
              description: The price of a single ticket for the event
            ticket_quantity:
              type: integer
              description: The total number of tickets available for the event
      - in: cookie
        name: session
        description: The session cookie used for authentication
        required: true
        type: string
    responses:
      200:
        description: Event created successfully
        schema:
          type: object
          properties:
            _id:
              type: string
              description: The unique identifier of the created event
            name:
              type: string
              description: The name of the created event
            description:
              type: string
              description: The description of the event
            location:
              type: string
              description: The location of the event
            start_date:
              type: string
              format: date
              description: The start date of the event
            end_date:
              type: string
              format: date
              description: The end date of the event
            start_time:
              type: string
              format: time
              description: The start time of the event
            end_time:
              type: string
              format: time
              description: The end time of the event
            ticket_price:
              type: integer
              description: The price of a ticket for the event
            ticket_quantity:
              type: integer
              description: The number of tickets available for the event
      400:
        description: Bad request. The event may already exist or missing data in the request.
      401:
        description: Unauthorized. Invalid session cookie.
      500:
        description: Internal server error
    """

    try:
        data = eventSchema.load(request.get_json())
        event = eventService.create_event(data)
        if event is None:
            return bad_response("Event Exist!")
        return good_response(event)

    except Exception as e:
        return exception_with_validation(e)


@event_bp.post("/guest")
@adminProtected
def add_guest_to_event():
    try:

        data = newGuestSchema.load(request.get_json())
        event = eventDAO.find_by_id(data.get("event_id"))

        guest_found = guestDAO.find_by_id(data.get("guest").get("guest_id"))

        if not guest_found:
            return bad_response("Guest not found!")

        if not event:
            return bad_response("Event not found")

        added = eventService.add_guest(data.get("event_id"), {
            "guest_id": guest_found["_id"],
            "name": guest_found["name"],
            "occupation": guest_found["occupation"],
            "sessions": data.get("guest").get("sessions")
        })

        print("Was added: ", added)

        if added:
            return good_response("Guests Added!")

    except Exception as e:
        return exception_with_validation(e)


@event_bp.post("/event_guest")
def get_event_guest_by_id():
    data = getEeventGuestSchema.load(request.get_json())
    guest_details = guestDAO.find_by_id(data["guest_id"])
    guest_in_event = eventDAO.find_guest_in_event(data["event_id"], data["guest_id"])

    if not guest_details:
        return bad_response("Guest not found!")

    if not guest_in_event:
        return bad_response("Guest not found in event")

    return good_response({
        **guest_details,
        "sessions": guest_in_event["sessions"]
    })


@event_bp.post("/cover/upload/<id>")
@adminProtected
def upload_events(id: str):
    # Check if the request contains a file
    try:
        found_event = eventDAO.find_by_id(id)
        if not found_event:
            return bad_response("Event not found!")

        if 'cover_image' not in request.files:
            return bad_response("File not found!")

        file = request.files['cover_image']

        # Check if a file is selected
        if file.filename == '':
            return bad_response("File not selected!")

        mime_type, _ = guess_type(file.filename)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        # Upload the file to Google Cloud Storage
        # try:
        file_data = file.read()
        response = upload_to_supabase(file_data, found_event["name"], mime_type)
        public_url = get_file_from_supabase(response.path)

        eventDAO.change_cover_image(found_event["_id"], public_url)

        return good_response({"cover_url": public_url})
    except Exception as e:
        return server_error()


@event_bp.post("/cover/<id>")
@adminProtected
def set_cover_url(id: str):
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

# @event_bp.get("/cover/<image>")
# def get_event_cover(image: str):
#     image_data, content_type = download_from_gcs(image)
#     return Response(image_data, content_type=content_type)
