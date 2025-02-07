from flask import session
from decouple import config
from utils.token import gen_token
from middlewares.auth import protectedRoute
import bcrypt
from .eventDAO import EventDAO
from utils.token import decode_token


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
        user = EventDAO().find_by_query({"email": email})
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
    

