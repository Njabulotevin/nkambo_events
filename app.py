from flask import Flask, make_response, render_template, request
from src.admin.adminController import admin_bp
from src.events.eventController import event_bp
from src.guests.guestController import guest_bp
from src.tickets.ticketController import ticket_bp

from decouple import config
from flask_session import Session
from flask_cors import CORS
from dotenv import load_dotenv
import os
from flasgger import Swagger

load_dotenv()
app = Flask(__name__)
# CORS(app)
# cors = CORS(app, resource={r"/*": {"origins": "*"}})
app.config["CORS_HEADERS"] = "Content-Type"

app.register_blueprint(admin_bp)
app.register_blueprint(event_bp)
app.register_blueprint(ticket_bp)
app.register_blueprint(guest_bp)

app.config["SECRET_KEY"] = config("SECRET_KEY")
app.config["DEBUG"] = config("DEBUG", default=False)
app.config["DATABASE_URI"] = config("PROD_DATABASE_URL") if os.getenv("ENVIRONMENT") == "production" else config(
    "DATABASE_URL")
app.config["SUPABASE_URL"] = config("SUPABASE_URL")
app.config["SUPABASE_KEY"] = config("SUPABASE_KEY")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_DOMAIN"] = "nkambo-events-ui-production.up.railway.app"
app.config["SESSION_FILE_DIR"] = "./flask_session_cache"
app.config['SESSION_COOKIE_SECURE'] = True
Session(app)

swagger = Swagger(app)


@app.after_request
def after_request_func(response):
    origin = request.headers.get("Origin")
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Credentials", "true")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Headers", "x-csrf-token")
        response.headers.add(
            "Access-Control-Allow-Methods", "POST, OPTIONS, PUT, PATCH, DELETE"
        )
        if origin:
            response.headers.add("Access-Control-Allow-Origin", origin)
    else:
        response.headers.add("Access-Control-Allow-Credentials", "true")
        if origin:
            response.headers.add("Access-Control-Allow-Origin", origin)

    return response


@app.route("/")
def index():
    return render_template("index.html")

application = app

if __name__ == "__main__":
    # with app.app_context():
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
