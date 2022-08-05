import os

from bson import ObjectId
from motor import motor_asyncio
from pymongo.collection import Collection

MONGODB_SERVER = os.getenv(MONGODB_SERVER)
MONGODB_USERNAME = os.getenv(MONGODB_USERNAME)
MONGODB_PASSWORD = os.getenv(MONGODB_PASSWORD)

MONGODB_CONNECTION_STRING = "mongodb+srv://{}:{}@{}}/?retryWrites=true&w=majority".format(
    MONGODB_USERNAME, MONGODB_PASSWORD, MONGODB_SERVER)

db = motor_asyncio.AsyncIOMotorClient(MONGODB_CONNECTION_STRING).get_database("ClimbHarder")
users_collection: Collection = db.get_collection("users")
workouts_collection: Collection = db.get_collection("workouts")


# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate
#
#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid objectid")
#         return ObjectId(v)
#
#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(type="string")
