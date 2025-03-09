from bson import ObjectId
from flask import Blueprint, request, session

from src.events.eventDAO import EventDAO

from .ticketModel import TicketSchema, Ticket
from utils.response import (
    bad_response,
    good_response,
    server_error,
    not_found,
    unauthorized,
)

from .ticketService import generate_ticket_number


from utils.token import gen_token, get_user_from_token
from middlewares.auth import adminProtected
import bcrypt
import uuid
from .ticketService import is_valid_user, get_user, is_ticket_redeemed
from .ticketDAO import TicketDAO
from marshmallow import ValidationError
from pymongo import errors


ticket_bp = Blueprint("ticket", __name__, url_prefix="/ticket")
eventDAO = EventDAO()
ticketDAO = TicketDAO()
ticketSchema = TicketSchema()


@ticket_bp.get("/")
def get_ticket():
    return good_response({"status": "all good"})


@ticket_bp.post("/buy/<id>")
def buya_a_ticket(id: str):

    try:
        found_event = eventDAO.find_by_id(id)
    
        if found_event != None:
            
            if int(found_event["ticket_quantity"]) == 0:
                return bad_response("Event Sold out!")
            
            data = ticketSchema.load(request.get_json())
            ticket = ticketDAO.save_ticket(
                {
                    "ticket_number": generate_ticket_number(found_event["name"]),
                    "event_id": found_event["_id"],
                    "attendee_name": data["attendee_name"],
                    "attendee_email": data["attendee_email"],
                    "is_redeemed": False,
                    "payment_id": None
                }
            )
            eventDAO.reduce_tickets(found_event["_id"])
            return good_response(ticket)
    
        return not_found("Event not found!")

    except Exception as e:
        print(e)
        return server_error()

@ticket_bp.get("/event/<event_id>")
@adminProtected
def get_event_tickets(event_id:str):
    try:
        tickets = ticketDAO.find_by_eventId(event_id)
        if tickets is None:
            return not_found("Event not found!")
        return good_response(tickets)
    except Exception as e:
        return server_error()

@ticket_bp.get("/redeem/<ticket_number>")
@adminProtected
def redeem_ticket(ticket_number: str):
    """
    Redeem a ticket using its ticket number
    ---
    parameters:
      - in: path
        name: ticket_number
        description: The unique ticket number to redeem
        required: true
        type: string

      - in: cookie
        name: session
        description: The session cookie used for authentication
        required: true
        type: string

    responses:
      200:
        description: Ticket successfully redeemed
        schema:
          type: object
          properties:
            ticket_number:
              type: string
              description: The unique ticket number
            event_id:
              type: string
              description: The unique identifier of the event
            attendee_name:
              type: string
              description: The name of the attendee
            attendee_email:
              type: string
              description: The email of the attendee
            is_redeemed:
              type: boolean
              description: The updated status of the ticket (redeemed)

      400:
        description: Ticket has already been redeemed or invalid ticket number
      404:
        description: Ticket not found
      500:
        description: Internal server error
    """
    try:
        is_redeemed, ticket = is_ticket_redeemed(ticket_number)
        if ticket:
            if is_redeemed:
                return bad_response("Redemption failed: This ticket has already been redeemed.")
            ticketDAO.redeem_ticket(ticket["_id"])
            return good_response({**ticket, "redeemed": True})

        return not_found("Redemption failed: Ticket not found. Please check the ticket code and try again.")

    except Exception as e:
        return server_error()
    


