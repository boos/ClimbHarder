import os

import pymongo
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
climbings_collection: Collection = db.get_collection("climbings")
hangboarding_collection: Collection = db.get_collection("hangboarding")


async def mongodb_initialization():
    # Ensure no user have the same username
    users_collection_indexes_keys = (await users_collection.index_information()).keys()
    if "unique_username" not in users_collection_indexes_keys:
        users_collection.create_index("username", name="unique_username", unique=True)

    # Ensure no user have the same username
    if "unique_email" not in users_collection_indexes_keys:
        users_collection.create_index("email", name="unique_email", unique=True)

    climbings_collection_indexes_keys = (await climbings_collection.index_information()).keys()
    if "unique_climbing_datetime" not in climbings_collection_indexes_keys:
        climbings_collection.create_index([("username", pymongo.ASCENDING), ("when", pymongo.DESCENDING)],
                                          name="unique_climbing_datetime",
                                          unique=True)

    hangboarding_collection_indexes_keys = (await hangboarding_collection.index_information()).keys()
    if "unique_hangboarding_datetime" not in hangboarding_collection_indexes_keys:
        hangboarding_collection.create_index([("username", pymongo.ASCENDING), ("when", pymongo.DESCENDING)],
                                             name="unique_hangboarding_datetime",
                                             unique=True)
