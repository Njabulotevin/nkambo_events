from pymongo import ASCENDING, DESCENDING
from database.database import DB_Collection
from bson import ObjectId
from .ticketModel import Ticket


class TicketDAO(DB_Collection):
    def __init__(self):
        super().__init__(collection_name="tickets")

    def save_ticket(self, item):
        ticket_id = self.collection.insert_one(item).inserted_id
        ticket = self.collection.find_one({"_id": ticket_id})
        return Ticket.serialize_ticket_db(ticket)

    def find_all(self):
        tickets = Ticket.serialize_ticket_db(self.collection.find())
        return tickets

    def find_by_id(self, id: str):
        try:
            ticket = self.collection.find_one({"_id": ObjectId(id)})
            if ticket:
                return Tciekt.serialize_ticket_db(ticket)
            return None
        except Exception as e:
            print(e)
            return None
    
    def find_by_query(self, query):
        ticket = self.collection.find_one(query)
        if ticket:
            return Ticket.serialize_ticket_db(ticket)
        return None
    
    def redeem_ticket(self, id):
        result = self.collection.update_one({"_id": ObjectId(id)}, {"$set": {"is_redeemed": True}})
        print("Results ", result)
        if result.modified_count == 1:
            return True
        return False
    
    def find_by_ticket_number(self, number):
        ticket = self.find_by_query({"ticket_number": number})
        if ticket:
            return ticket
        return None
        
    def find_all_by_query(self, query):
        tickets = self.collection.find(query)
        if tickets:
            return Ticket.serialize_tickets_db(tickets)
        return None
