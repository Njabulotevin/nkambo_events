from flask import Blueprint, request, session
from utils.response import bad_response, good_response, server_error, not_found, unauthorized
from utils.token import is_admin
# from decouple import config
from utils.token import gen_token
from middlewares.auth import protectedRoute
import bcrypt
import uuid
from .adminService import is_valid_admin, get_admin
from .adminDAO import AdminDAO
from .adminModel import Token_validator
from marshmallow import ValidationError


admin_bp = Blueprint("admin", __name__, url_prefix='/admin')

token_Validator = Token_validator()

@admin_bp.get("/<id>")
def get_admin_controller(id: str):
    """
    Get details of an admin user by ID.
    ---
    parameters:
      - in: path
        name: id
        description: The unique identifier of the admin user
        required: true
        type: string
    responses:
      200:
        description: Admin details retrieved successfully
        schema:
          type: object
          properties:
            _id:
              type: string
              description: The unique identifier of the admin
            email:
              type: string
              description: The email of the admin
            username:
              type: string
              description: The username of the admin
      404:
        description: Admin not found
      500:
        description: Internal server error
    """
    try:
        admin = AdminDAO().find_by_id(str(id))
        return good_response(admin)
    except Exception as e:
        print(e)
        return server_error()


@admin_bp.post("/login")
def login():
    """
    Admin login endpoint to authenticate and generate a session token.
    ---
    parameters:
      - in: body
        name: credentials
        description: The login credentials (email and password) for the admin
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: Admin's email address
            password:
              type: string
              description: Admin's password
    responses:
      200:
        description: Successful login with token
        schema:
          type: object
          properties:
            admin:
              type: object
              description: The authenticated admin's details
            token:
              type: string
              description: JWT token for authentication
      400:
        description: Invalid email or password
      500:
        description: Server error
    """
    try:
        data = request.get_json()
        email, password = data["email"], data["password"]
        admin = is_valid_admin(email, password)
        if admin:
            token = gen_token(admin, "admin")
            session["token"] = token
            print(token)
            return good_response({"admin": admin, "token": token})
        return bad_response("Invalid email or password")
    except Exception as e:
        if isinstance(e, KeyError):
            return bad_response(f"The following fields are missing: {e}")
        print(e)
        return "Server error", 500


@admin_bp.post("/register")
def register():
    """
    Register a new admin user.
    ---
    parameters:
      - in: body
        name: admin_data
        description: The details required to register a new admin
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: Admin's email address
            username:
              type: string
              description: Admin's chosen username
            password:
              type: string
              description: Admin's password
    responses:
      200:
        description: Admin registered successfully
        schema:
          type: object
          properties:
            admin:
              type: object
              description: The newly registered admin's details
      400:
        description: Admin already exists or missing required fields
      500:
        description: Internal server error
    """
    try:
        data = request.get_json()
        email, username, password = data["email"], data["username"], data["password"]
        password = password.encode("utf8")
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(password, salt)

        admin = get_admin(email=email)
        if admin:
            return bad_response("Admin already exists!")

        admin = AdminDAO().insert(
            {"email": email, "password": hashed_pw.decode("utf8")})
        admin.pop("password")
        return good_response({"admin": admin})
    except Exception as e:
        print(e)
        if "UNIQUE constraint failed: admin.email" in str(e):
            return bad_response("Admin already exists!")
        return server_error()

@admin_bp.post("/validate/token")
def validate():
    try:
        data = token_Validator.load(request.get_json())
        is_valid = is_admin(data["token"])
        if is_valid:
            return good_response({"token": data["token"], "is_valid": True})
        return bad_response("Invalid token")

    except Exception as e:
        print(e)
        if isinstance(e, ValidationError):
            return bad_response(e.messages)
        return server_error()


