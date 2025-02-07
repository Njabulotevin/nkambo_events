from database.db_conn import get_database
from enum import Enum


class UpdateOperation(Enum):
    PUSH = "$push"
    ADD_TO_SET = "$addToSet"
    PULL = "$pull"
    PULL_ALL = "$pullAll"
    POP = "$pop"
    INC = "$inc"
    MUL = "$mul"
    MIN = "$min"
    MAX = "$max"
    SET = "$set"
    UNSET = "$unset"


class DB_Collection:
    def __init__(self, collection_name):
        connect_db = get_database()
        self.db = connect_db["nkambo_events"]
        self.collection = self.db[collection_name]
