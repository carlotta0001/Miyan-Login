from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from app.core import config

client = MongoClient(config.MONGO_URI, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client[config.DB_NAME]
users_collection = db["users"]

def add_key(key, expires_at):
    if users_collection.find_one({"key": key}):
        return False
    users_collection.insert_one({
        "key": key,
        "device_id": None,
        "created_at": datetime.utcnow(),
        "expires_at": expires_at
    })
    return True

def set_key_expiration(key, expires_at):
    result = users_collection.update_one(
        {"key": key},
        {"$set": {"expires_at": expires_at}}
    )
    return result.matched_count > 0

def remove_key(key):
    result = users_collection.delete_one({"key": key})
    return result.deleted_count > 0

def reset_device_id(key):
    result = users_collection.update_one(
        {"key": key},
        {"$set": {"device_id": None}}
    )
    return result.matched_count > 0

def get_key_info(key):
    return users_collection.find_one({"key": key}, {"_id": 0})

def get_all_keys():
    keys = users_collection.find({}, {"_id": 0, "key": 1, "device_id": 1, "expires_at": 1})
    return list(keys)

def verify_and_update_device(key, device_id):
    user = users_collection.find_one({"key": key})

    if not user:
        return {"status": "error", "message": "Invalid key."}

    expiry_date = user.get("expires_at")
    if expiry_date and expiry_date < datetime.utcnow():
        users_collection.delete_one({"_id": user["_id"]})
        return {"status": "error", "message": "Key has expired and has been removed."}

    if user.get("device_id") and user["device_id"] != device_id:
        return {"status": "error", "message": "Key is already registered to another device."}

    if not user.get("device_id"):
        users_collection.update_one({"key": key}, {"$set": {"device_id": device_id}})
        return {
            "status": "success",
            "message": "Login successful, device has been registered.",
            "expiry": expiry_date
        }

    return {
        "status": "success",
        "message": "Login successful.",
        "expiry": expiry_date
    }