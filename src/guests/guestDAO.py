from pymongo import ASCENDING, DESCENDING
from database.database import DB_Collection
from bson import ObjectId

from src.guests.guestModel import Guest


class GuestDAO(DB_Collection):
    def __init__(self):
        super().__init__(collection_name="guests")

    def save_guest(self, item):
        guest_id = self.collection.insert_one(item).inserted_id
        guest = self.collection.find_one({"_id": guest_id})
        return Guest.serialize_guest_db(guest)

    def find_all(self):
        guests = Guest.serialize_guests_db(self.collection.find())
        return guests

    def find_by_id(self, id: str):
        try:
            guest = self.collection.find_one({"_id": ObjectId(id)})
            if guest:
                return Guest.serialize_guest_db(guest)
            return None
        except Exception as e:
            print(e)
            return None

    def find_by_eventId(self, eventId):
        return self.find_all_by_query({"event_id": eventId})

    def find_by_query(self, query):
        guest = self.collection.find_one(query)
        if guest:
            return Guest.serialize_guest_db(guest)
        return None

    def find_by_guest_number(self, number):
        guest = self.find_by_query({"guest_number": number})
        if guest:
            return guest
        return None

    def find_all_by_query(self, query):
        guests = self.collection.find(query)
        if guests:
            return Guest.serialize_guests_db(guests)
        return None
