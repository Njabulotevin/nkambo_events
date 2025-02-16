from flask import session
from decouple import config
from utils.token import gen_token
from middlewares.auth import protectedRoute
import bcrypt
from utils.token import decode_token

from google.cloud import storage
from datetime import timedelta
from google.oauth2 import service_account
import os
import base64




encoded_credentials = os.getenv("SERVICE_ACCOUNT_SETTINGS")
decoded_credentials = base64.b64decode(encoded_credentials)

# Save it to a temporary file
with open('/tmp/service-account.json', 'wb') as f:
    f.write(decoded_credentials)


credentials = service_account.Credentials.from_service_account_file(
    '/tmp/service-account.json'
)

# Initialize Google Cloud Storage client
client = storage.Client(credentials=credentials, project='nkambo-events-451018')

# Set your Google Cloud bucket name
bucket_name = 'nkambo-events-bucket'


def upload_file_to_gcs(file):
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob("nkambo-event-"+file.filename)
    blob.upload_from_file(file)
    return blob.name

def upload_event_cover_image(file, event):
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(event["name"].replace(" ", "-").lower()+"-"+event["_id"]+"-"+file.filename)
    blob.upload_from_file(file)
    return blob.name

def download_from_gcs(source_blob_name):
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    return blob.download_as_bytes(), blob.content_type

    