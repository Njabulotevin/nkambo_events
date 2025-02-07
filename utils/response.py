from flask import make_response


def response(data, status_code):
    response = make_response(data)
    response.status_code = status_code
    response.headers["Content-Type"] = "application/json"
    # response.headers.add("Access-Control-Allow-Origin", "*")
    # response.headers.add('Access-Control-Allow-Headers', "*")
    # response.headers.add('Access-Control-Allow-Methods', "*")
    return response


def bad_response(message):
    return response({"status": 400, "message": message}, 400)


def good_response(data):
    return response({"status": 200, "data": data}, 200)


def unauthorized():
    return response({"status": 401, "message": "Unauthorised!"}, 401)


def not_found(message="Not Found!"):
    return response({"status": 404, "message": message}, 404)


def server_error():
    return response({"status": 500, "message": "Server error!"}, 500)
