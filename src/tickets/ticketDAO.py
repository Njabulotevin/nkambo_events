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

    # def find_all(self):
    #     subjects = Subject.serialize_subjects_db(self.collection.find())
    #     return subjects

    # def find_by_id(self, id: str):
    #     try:
    #         user = self.collection.find_one({"_id": ObjectId(id)})
    #         if user:
    #             return Subject.serialize_subject_db(user)
    #         return None
    #     except Exception as e:
    #         print(e)
    #         return None

    # def add_student(self, student, subject_id):
    #     try:
    #         updated = self.collection.update_one(
    #             {
    #                 "_id": ObjectId(subject_id),
    #             },
    #             {"$addToSet": {"students": student}},
    #         ).modified_count
    #         return updated
    #     except Exception as e:
    #         return 0
    

    # def find_by_query(self, query):
    #     subject = self.collection.find_one(query)
    #     if subject:
    #         return Subject.serialize_subject_db(subject)
    #     return None
    
    # def find_all_by_query(self, query):
    #     subjects = self.collection.find(query)
    #     if subjects:
    #         return Subject.serialize_subjects_db(subjects)
    #     return None
