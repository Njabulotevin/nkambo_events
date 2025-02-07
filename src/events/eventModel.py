from bson import ObjectId
from marshmallow import Schema, fields, ValidationError


class Event:
    def __init__(
        self,
        name: str,
        description: str,
        event_date: str,  # Added event_date field
        location: str,  # Added location field
        time: str,
        date: str,
        price: str,
    ) -> None:
        self.name = name
        self.description = description
        self.event_date = event_date
        self.location = location
        self.time = time
        self.date = date
        self.price = price

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "event_date": self.event_date,
            "location": self.location,
        }

    @classmethod
    def create_event(cls, event_data):
        return cls(
            name=event_data["name"].lower(),
            description=event_data["description"],
            event_date=event_data["event_date"],  # Ensure event_date is included
            location=event_data["location"],  # Ensure location is included,
            date=event_data["date"],
            time=event_data["time"],
            price=event_data["price"],
        )

    @classmethod
    def serialize_event_db(cls, event_dict):
        if event_dict:
            return {
                "_id": str(event_dict["_id"]),
                "name": event_dict["name"],
                "description": event_dict["description"],
                "event_date": event_dict["event_date"],
                "location": event_dict["location"],
                "date": event_dict["date"],
                "time": event_dict["time"],
                "price": event_dict["price"],
            }
        return None

    @classmethod
    def serialize_events_db(cls, events: list) -> list:
        """
        Serialize a list of MongoDB events.
        """
        return [cls.serialize_event_db(event) for event in events]


class EventSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    event_date = fields.Str(required=True)  # Ensures event_date is validated
    location = fields.Str(required=True)  # Ensures location is 
    date=fields.Str(required=True)
    time=fields.Str(required=True)
    price=fields.Str(required=True)
