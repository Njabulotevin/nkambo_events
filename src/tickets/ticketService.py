from flask import session
from decouple import config
from utils.token import gen_token
from middlewares.auth import protectedRoute
import bcrypt
from .ticketDAO import TicketDAO
from utils.token import decode_token
import random
import string


def is_valid_user(email: str, password: str):
    try:
        user = get_user(email=email)
        password_correct = bcrypt.checkpw(password.encode(
            "utf8"), user["password"].encode("utf8"))
        if user:
            if email == user["email"] and password_correct:
                user.pop("password")
                return user
    except Exception as e:
        print(e)
        return False



def get_user(id=None, email=None) -> dict:
    try:
        user = TicketDAO().find_by_query({"email": email})
        if user:
            return user
        return None
    except Exception as e:
        # print("From Alchemy: ", e)
        return None


def get_user_id():
    try:
        return decode_token(session.get("token")).get("user").get("_id")
    except Exception as e:
        print(e)
        return None
    
def generate_ticket_number(event_name: str):
    words = event_name.split()
    prefix = (words[0][:2] if len(words) == 1 else words[0][0] + words[1][0]).upper()
    digits = "".join(random.choices(string.digits, k=3))
    suffix = "".join(random.choices(string.ascii_uppercase, k=3))
    return f"{prefix}{digits}{suffix}"
