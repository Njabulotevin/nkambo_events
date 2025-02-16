from bson import ObjectId
from marshmallow import Schema, fields, ValidationError

class Ticket:
    def __init__(
        self,
        ticket_number: str,
        event_id: str,
        attendee_name: str,
        attendee_email: str,
        is_redeemed: bool
        
    ) -> None:
        self.ticket_number = ticket_number
        self.event_id = event_id
        self.attendee_name = attendee_name
        self.email = email
        self.is_redeemed: is_redeemed

    def to_dict(self):
        return {
            "ticket_number": self.ticket_number,
            "event_name": self.event_name,
            "attendee_name": self.attendee_name,
            "attendee_email": self.email,
            "is_redeemed": self.is_redeemed
        }

    @classmethod
    def create_ticket(cls, ticket_data):
        return cls(
            ticket_number=ticket_data['ticket_number'],  # Generate a unique ticket number
            event_id=ticket_data["event_id"],
            attendee_name=ticket_data["attendee_name"],
            attendee_nemail=ticket_data["attendee_email"],
            is_redeemed=ticket_data["is_redeemed"]
        )

    @classmethod
    def serialize_ticket_db(cls, ticket_dict):
        if ticket_dict:
            return {
                "_id": str(ticket_dict["_id"]),
                "ticket_number": ticket_dict["ticket_number"],
                "event_id": ticket_dict["event_id"],
                "attendee_name": ticket_dict["attendee_name"],
                "attendee_email": ticket_dict["attendee_email"],
                "is_redeemed": ticket_dict["is_redeemed"]
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


    


    
    


    
    
