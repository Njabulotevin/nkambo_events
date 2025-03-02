from bson import ObjectId
from marshmallow import Schema, fields, ValidationError


class Event:
    def __init__(
        self,
        name: str,
        description: str,
        location: str, 
        start_time: str,
        end_time: str,
        start_date: str,
        end_date: str,
        ticket_price: str,
        ticket_quantity: int,
        cover_url:str
        
    ) -> None:
        self.name = name
        self.description = description
        self.location = location
        self.start_time = start_time
        self.end_time = end_time
        self.start_date = start_date
        self.end_date = end_date
        self.ticket_price = ticket_price
        self.ticket_quantity = ticket_quantity
        self.cover_url = cover_url

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "ticket_price": self.ticket_price,
            "ticket_quantity": self.ticket_quantity,
            "cover_url": self.cover_url
        }

    @classmethod
    def create_event(cls, event_data):
        return cls(
            name=event_data["name"].lower(),
            description=event_data["description"],
            location=event_data["location"],  # Ensure location is included,
            start_time=event_data["start_time"],
            end_time=event_data["end_time"],
            start_date=event_data["start_date"],
            end_date=event_data["end_date"],
            ticket_quantity = event_data["ticket_quantity"],
            cover_url = event_data["cover_url"]
        )

    @classmethod
    def serialize_event_db(cls, event_dict):
        if event_dict:
            return {
                "_id": str(event_dict["_id"]),
                "name": event_dict["name"],
                "description": event_dict["description"],
                "location": event_dict["location"],
                "start_date": event_dict["start_date"],
                "end_date": event_dict["end_date"],
                "start_time": event_dict["start_time"],
                "end_time": event_dict["end_time"],
                "ticket_price": event_dict["ticket_price"],
                "ticket_quantity" : event_dict["ticket_quantity"],
                "cover_url": event_dict["cover_url"]
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
    location = fields.Str(required=True)
    start_date=fields.Str(required=True)
    end_date=fields.Str(required=True)
    start_time=fields.Str(required=True)
    end_time=fields.Str(required=True)
    ticket_price=fields.Int(required=True)
    ticket_quantity=fields.Int(required=True)
    

class EventCoverSchema(Schema):
    cover_url = fields.Str(required=True)
    