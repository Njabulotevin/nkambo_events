from flask import Blueprint, request, session
from utils.response import bad_response, good_response, server_error, not_found, unauthorized
# from decouple import config
from utils.token import gen_token
from middlewares.auth import protectedRoute
import bcrypt
import uuid
from .adminService import is_valid_admin, get_admin
from .adminDAO import AdminDAO


admin_bp = Blueprint("admin", __name__, url_prefix='/admin')


@admin_bp.get("/<id>")
def get_admin_controller(id: str):
    try:
        admin = AdminDAO().find_by_id(str(id))
        return good_response(admin)
    except Exception as e:
        print(e)
        return server_error()


@admin_bp.post("/login")
def login():
    try:
        data = request.get_json()
        email, password = data["email"], data["password"]
        admin = is_valid_admin(email, password)
        if admin:
            token = gen_token(admin, "admin")
            session["token"] = token
            print(token)
            return good_response({"admin": admin})
        return bad_response("Invalid email or password")
    except Exception as e:
        if isinstance(e, KeyError):
            return bad_response(f"The following fields are missing: {e}")
        print(e)
        return "Server error", 500


@admin_bp.post("/register")
def register():
    try:
        data = request.get_json()
        email, username, password = data["email"], data["username"], data["password"]
        password = password.encode("utf8")
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(password, salt)

        admin = get_admin(email=email)
        if admin:
            return bad_response("admin Already exist!")

        admin = AdminDAO().insert(
            {"email": email, "password": hashed_pw.decode("utf8")})
        admin.pop("password")
        return good_response({"admin": admin})
    except Exception as e:
        print(e)
        if "UNIQUE constraint failed: admin.email" in str(e):
            return bad_response("admin already exist!")
        return server_error()
