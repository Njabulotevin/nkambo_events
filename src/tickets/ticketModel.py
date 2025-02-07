from bson import ObjectId
from marshmallow import Schema, fields, ValidationError

class Ticket:
    def __init__(
        self,
        ticket_number: str,
        event_name: str,
        description: str,
        attendee_name: str,
        email: str,
        location: str,
        event_time: str,
        event_date: str,
        ticket_price:str
    ) -> None:
        self.ticket_number = ticket_number
        self.event_name = event_name
        self.description = description
        self.attendee_name = attendee_name
        self.email = email
        self.location = location
        self.event_time = event_time
        self.event_date = event_date
        self.ticket_price = ticket_price

    def to_dict(self):
        return {
            "ticket_number": self.ticket_number,
            "event_name": self.event_name,
            "description": self.description,
            "attendee_name": self.attendee_name,
            "attendee_email": self.email,
            "ticket_price": self.ticket_price,
            "location": self.location,
            "event_time": self.event_time,
        }

    @classmethod
    def create_ticket(cls, ticket_data):
        return cls(
            ticket_number=ticket_data['ticket_number'],  # Generate a unique ticket number
            event_name=ticket_data["event_name"],
            description=ticket_data["description"],
            attendee_name=ticket_data["attendee_name"],
            email=ticket_data["attendee_email"],
            location=ticket_data["location"],
            event_date=ticket_data["event_date"],
            event_time=ticket_data["event_time"],
            ticket_price=ticket_data["ticket_price"]
        )

    @classmethod
    def serialize_ticket_db(cls, ticket_dict):
        if ticket_dict:
            return {
                "_id": str(ticket_dict["_id"]),
                "ticket_number": ticket_dict["ticket_number"],
                "event_name": ticket_dict["event_name"],
                "description": ticket_dict["description"],
                "attendee_name": ticket_dict["attendee_name"],
                "attendee_email": ticket_dict["attendee_email"],
                "location": ticket_dict["location"],
                "event_time": ticket_dict["event_time"],
                "event_date": ticket_dict["event_date"],
                "ticket_price": ticket_dict["ticket_price"],
            }
        return None

    @classmethod
    def serialize_tickets_db(cls, tickets: list) -> list:
        """
        Serialize a list of MongoDB tickets.
        """
        return [cls.serialize_ticket_db(ticket) for ticket in tickets]


class TicketSchema(Schema):
    attendee_name = fields.Str(required=True)
    attendee_email = fields.Email(required=True)


    


    
    


    
    
