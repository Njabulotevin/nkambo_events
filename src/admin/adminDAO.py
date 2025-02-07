from database.database import DB_Collection
from bson import ObjectId
from .adminModel import Admin


class AdminDAO(DB_Collection):
    def __init__(self):
        super().__init__(collection_name="admins")

    def insert(self, item):
        admin_id = self.collection.insert_one(item).inserted_id
        admin = self.collection.find_one({"_id": admin_id})
        return Admin.serialize_admin_db(admin)

    def find_all(self):
        admins = Admin.serialize_admins_db(self.collection.find())
        return admins

    def find_by_id(self, id: str):
        try:
            admin = self.collection.find_one({"_id": ObjectId(id)})
            if admin:
                return Admin.serialize_admin_db(admin)
            return None
        except Exception as e:
            print(e)
            return None

    def find_by_query(self, query):
        admin = self.collection.find_one(query)
        return Admin.serialize_admin_db(admin)
