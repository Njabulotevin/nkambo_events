from flask import session
from decouple import config
from utils.token import gen_token
from middlewares.auth import protectedRoute
import bcrypt
from .adminDAO import AdminDAO
from utils.token import decode_token


def is_valid_admin(email: str, password: str):
    try:
        admin = get_admin(email=email)
        password_correct = bcrypt.checkpw(password.encode(
            "utf8"), admin["password"].encode("utf8"))
        if admin:
            if email == admin["email"] and password_correct:
                admin.pop("password")
                return admin
    except Exception as e:
        print(e)
        return False



def get_admin(id=None, email=None) -> dict:
    try:
        admin = AdminDAO().find_by_query({"email": email})
        if admin:
            return admin
        return None
    except Exception as e:
        # print("From Alchemy: ", e)
        return None


def get_admin_id():
    try:
        return decode_token(session.get("token")).get("admin").get("_id")
    except Exception as e:
        print(e)
        return None
