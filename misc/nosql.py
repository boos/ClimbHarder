import os

from motor import motor_asyncio
from pymongo.collection import Collection

MONGODB_SERVER = os.getenv("MONGODB_SERVER")
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")

MONGODB_CONNECTION_STRING = "mongodb+srv://{}:{}@{}/?retryWrites=true&w=majority".format(MONGODB_USERNAME,
                                                                                         MONGODB_PASSWORD,
                                                                                         MONGODB_SERVER)

db = motor_asyncio.AsyncIOMotorClient(MONGODB_CONNECTION_STRING).get_database("ClimbHarder")
users_collection: Collection = db.get_collection("users")
workouts_collection: Collection = db.get_collection("workouts")


async def mongodb_initialization():
    users_collection_indexes_keys = (await users_collection.index_information()).keys()
    if "unique_username" not in users_collection_indexes_keys:
        users_collection.create_index("username", name="unique_username", unique=True)

    if "unique_email" not in users_collection_indexes_keys:
        users_collection.create_index("email", name="unique_email", unique=True)
