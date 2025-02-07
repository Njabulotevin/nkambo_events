import bcrypt
from decouple import config
import datetime
import jwt


def gen_token(data, role):
    secret = config("SECRET_KEY")
    payload = {"sub": role ,"user": data, "exp":  datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=3)}
    return jwt.encode(payload, secret, algorithm="HS256")


def is_valid_token(token):

    try:
    # Verify and decode the JWT
        decoded_payload = decode_token(token)
    # The token is valid, and you can access its data in the `decoded_payload` dictionary.
        return True
    except jwt.ExpiredSignatureError:
        # Token has expired
        return "expired"
    except jwt.DecodeError:
        return "invalid"
    


def decode_token(token):
    secret = config("SECRET_KEY")
    try:
        decoded_payload = jwt.decode(token, secret, algorithms=["HS256"])
        return decoded_payload
    except Exception as e:
        print(e)
        return None
    
    
def hash_password(password:str):
    plain_password = password.encode("utf8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password, salt)
     

def is_allowed_role(token, target_role):
    try:
        # Verify and decode the JWT
        decoded_payload = decode_token(token)

        # Extract the role from the payload
        role = decoded_payload["sub"]

        # Check if the user's role matches the target role or is an admin
        if role == str(target_role) or role == "admin":
            return True
        return False

    except jwt.ExpiredSignatureError:
        # Token has expired
        return "expired"

    except jwt.DecodeError:
        # Token is invalid
        return "invalid"
    
    
def is_admin(token):
    try:
        decoded_payload = decode_token(token)
        if decoded_payload:
            role = decoded_payload["sub"]
            if role == "admin":
                return True
        return False

    except jwt.ExpiredSignatureError:
        # Token has expired
        return "expired"

    except jwt.DecodeError:
        # Token is invalid
        return "invalid"
    

def is_instructor(token):
    try:
        decoded_payload = decode_token(token)
        if decoded_payload:
            role = decoded_payload["sub"]
            if role=="instructor" or role == "admin":
                return True
        return False

    except jwt.ExpiredSignatureError:
        # Token has expired
        return "expired"

    except jwt.DecodeError:
        # Token is invalid
        return "invalid"

def is_student(token):
    try:
        decoded_payload = decode_token(token)
        if decoded_payload:
            role = decoded_payload["sub"]
            if role=="student" or role == "admin" or role=="instructor":
                return True
        return False

    except jwt.ExpiredSignatureError:
        # Token has expired
        return "expired"

    except jwt.DecodeError:
        # Token is invalid
        return "invalid"

    

def get_user_from_token(token):
    return decode_token(token)["user"]