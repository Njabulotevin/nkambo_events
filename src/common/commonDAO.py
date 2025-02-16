from pymongo import ASCENDING, DESCENDING
from database.database import DB_Collection
from bson import ObjectId
from .eventModel import Event


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

    def find_by_id(self, id: str):
        try:
            event = self.collection.find_one({"_id": ObjectId(id)})
            if event:
                return Event.serialize_event_db(event)
            return None
        except Exception as e:
            print(e)
            return None
 

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
