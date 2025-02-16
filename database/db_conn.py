from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from decouple import config
import os


def get_database():
   uri = config("PROD_DATABASE_URL") if os.getenv("ENVIRONMENT") == "production" else config("DATABASE_URL")
   # Create a new client and connect to the server
   client = MongoClient(uri, server_api=ServerApi('1'))

   # Send a ping to confirm a successful connection
   try:
      client.admin.command('ping')
      print("Pinged your deployment. You successfully connected to MongoDB!")
      return client
   except Exception as e:
      print(e)





  