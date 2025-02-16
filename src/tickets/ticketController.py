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


@ticket_bp.post("/create/<id>")
def create_ticket(id: str):
    try:
        found_event = eventDAO.find_by_id(id)
        print("event found ", found_event)

        if found_event != None:
            
            data = ticketSchema.load(request.get_json())

            ticket = ticketDAO.save_ticket(
                {
                    "ticket_number": generate_ticket_number(found_event["name"]),
                    "event_id": found_event["_id"],
                    "attendee_name": data["attendee_name"],
                    "attendee_email": data["attendee_email"],
                    "is_redeemed": False
                }
            )
            return good_response(ticket)
    
        return not_found("Event not found!")

    except Exception as e:
        print(e)
        return server_error()

@ticket_bp.get("/redeem/<ticket_number>")
@adminProtected
def redeem_ticket(ticket_number: str):
    try:
        is_redeemed, ticket = is_ticket_redeemed(ticket_number)
        if ticket:
            if is_redeemed:
                return bad_response("Ticket already redeemed!")
            ticketDAO.redeem_ticket(ticket["_id"])
            return good_response({**ticket, "redeemed": True})
        
        return not_found("Ticket not found")
    except Exception as e:
        return server_error()
    


# @event_bp.post("/create")
# @instructorProtected
# def register():
#     try:
#         data = subjectSchema.load(request.get_json())
#         token = session["token"]

#         grade = _gradeDAO.find_by_query({"grade": data["grade"]})

#         if not grade:
#             return bad_response("Grade not found!")

#         user = get_user_from_token(token)

#         subject = Subject.create_subject(
#             {
#                 "name": data["name"],
#                 "description": data["description"],
#                 "grade": grade["grade"],
#                 "instructor": user["_id"],
#             }
#         )

#         subject_in_grade = _gradeDAO.find_by_query({"subjects.name": subject.name})

#         if subject_in_grade:
#             return bad_response("Subject already exist")

#         added_subject = subjectDAO.insert(subject.to_dict())
#         grade_subject = {"_id": added_subject["_id"], "name": added_subject["name"]}

#         update_grade = _gradeDAO.add_subject(data["grade"], grade_subject)
#         return good_response(update_grade)

#     except Exception as e:
#         print(e)
#         if isinstance(e, ValidationError):
#             return bad_response(e.messages)
#         elif isinstance(e, errors.DuplicateKeyError):
#             return bad_response("Subject already exist")
#         return server_error()


# @event_bp.get("/<id>")
# def get_subjects(id: str):
#     try:
#         subject = subjectDAO.find_by_id(id)
#         if not subject:
#             return not_found()
#         return good_response(subject)
#     except Exception as e:
#         return server_error()


# @event_bp.get("/")
# def get_all_subjects():
#     try:
#         subjects = subjectDAO.find_all()
#         return good_response(subjects)
#     except Exception as e:
#         return server_error()


# @event_bp.post("/add/student")
# @instructorProtected
# def add_students():
#     try:
#         data = studentSubjectSchema.load(request.get_json())
#         student = _studentDAO.find_by_id(data["student_id"])
#         if not student:
#             return bad_response("Student not found!")
#         grade = _gradeDAO.find_by_query({"grade": student["student_details"]["grade"]})
#         if not grade:
#             return bad_response("Grade not found!")

#         subject = subjectDAO.find_by_query(
#             {"grade": grade["grade"], "name": data["subject_name"]}
#         )
#         if not subject:
#             return bad_response("Subject not found!")
#         updated_count = subjectDAO.add_student(
#             subject_id=subject["_id"], student={"student_id": student["_id"]}
#         )
#         if not updated_count > 0:
#             return bad_response("Student not added, student exit!")
#         return good_response("Ok")
#     except ValidationError as e:
#         return bad_response(e.messages)
#     except Exception as e:
#         print("Error occurred:", str(e))
#         return server_error()


# @event_bp.get("/student/<id>")
# def get_student_subject(id : str):
#     subjects = subjectDAO.find_all_by_query({"students.student_id": id})
#     if subjects:
#         for subject in subjects:
#             subject.pop("students")
#     print(subjects)
#     return good_response(subjects)
