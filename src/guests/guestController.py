from flask import Blueprint, request

from middlewares.auth import adminProtected
from src.guests.guestDAO import GuestDAO
from src.guests.guestModel import GuestSchema
from utils.errors import exception_with_validation
from utils.response import good_response, not_found, server_error

guest_bp = Blueprint("guest", __name__, url_prefix="/guest")

guestDAO = GuestDAO()

guestSchema = GuestSchema()


@guest_bp.get("/")
def get_all_guests():
    try:
        guests = guestDAO.find_all()
        return good_response(guests)
    except Exception as e:
        print(e)
        return server_error()


@guest_bp.post("/")
@adminProtected
def add_new_guest():
    try:
        data = guestSchema.load(request.get_json())
        added_guest = guestDAO.save_guest(data)

        print("Guest was created: ", added_guest)

        return good_response(added_guest)
    except Exception as e:
        return exception_with_validation(e)


@guest_bp.get("/<id>")
def get_guest_by_id(id: str):
    try:
        guest_found = guestDAO.find_by_id(id)

        if not guest_found:
            return not_found()

        return good_response(guest_found)

    except Exception as e:
        return exception_with_validation(e)
