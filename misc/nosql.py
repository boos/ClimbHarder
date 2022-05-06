from bson import ObjectId
from motor import motor_asyncio
from motor.motor_asyncio import AsyncIOMotorCollection

db = motor_asyncio.AsyncIOMotorClient(
    'mongodb://nuc:27017/').get_database("ClimbHarder")
users_collection = db.get_collection("users")


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
