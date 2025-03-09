from pymongo import ASCENDING, DESCENDING
from database.database import DB_Collection
from bson import ObjectId
from .eventModel import Event, EventGuestSchema, EventGuest
from ..guests.guestModel import Guest


class EventDAO(DB_Collection):
    def __init__(self):
        super().__init__(collection_name="events")

    def save_event(self, item):
        event_id = self.collection.insert_one(item).inserted_id
        event = self.collection.find_one({"_id": event_id})
        return Event.serialize_event_db(event)

    def find_all(self):
        events = Event.serialize_events_db(self.collection.find())
        return events

    def find_by_id(self, event_id: str):
        try:
            event = self.collection.find_one({"_id": ObjectId(event_id)})
            if event:
                return Event.serialize_event_db(event)
            return None
        except Exception as e:
            print(e)
            return None

    def change_cover_image(self, event_id, cover_url):
        result = self.collection.update_one({"_id": ObjectId(event_id)}, {"$set": {"cover_url": cover_url}})
        print("Results ", result)
        if result.modified_count == 1:
            return True
        return False

    def save_guest(self, event_id: str, guest):
        result = self.collection.update_one({"_id": ObjectId(event_id)}, {"$addToSet": {"guest_speaker": guest}})
        if result.modified_count == 1:
            return True
        return False

    def find_guest_in_event(self, event_id, guest_id):
        result = self.collection.find_one(
            {
                "_id": ObjectId(event_id),
                "guest_speaker.guest_id": guest_id
            },
            {"guest_speaker": {"$elemMatch": {"guest_id": guest_id}}}
        )

        if result:
            return Event.serialize_event_guest_db(result)

        return None

    def reduce_tickets(self, id):
        result = self.collection.update_one({"_id": ObjectId(id)}, {"$inc": {"ticket_quantity": -1}})
        if result.modified_count == 1:
            return True
        return False

    def find_by_query(self, query):
        event = self.collection.find_one(query)
        if event:
            return Event.serialize_event_db(event)
        return None

    def find_all_by_query(self, query):
        events = self.collection.find(query)
        if events:
            return Event.serialize_events_db(events)
        return None
