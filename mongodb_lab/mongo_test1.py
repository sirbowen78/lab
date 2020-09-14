from pymongo import MongoClient
from bson.objectid import ObjectId

# Examples on how to delete multiple entries by id.
mongodb_url = "mongodb://192.168.1.211:27017"

mclient = MongoClient(mongodb_url)
mdb = mclient["first_db"]
mtable = mdb["device"]
del_query = {
    "_id": {
        "$in": [ObjectId('5f5f81a15998e89f89e0ea77'),
                ObjectId('5f5f81a15998e89f89e0ea78'),
                ObjectId('5f5f81a359c82df6500a3559')]
    }
}
mtable.delete_many(del_query)
for x in mtable.find():
    print(x)