from pymongo import MongoClient

MONGO_URI = ""mongodb+srv://Paidii:Paidisetty%4010@cluster0.kfocv.mongodb.net/""

database1_name = "Dummy"
database2_name = "Dummy_1"

client = MongoClient(MONGO_URI)

db1_collections = set(client[database1_name].list_collection_names())
db2_collections = set(client[database2_name].list_collection_names())

collections_only_in_db1 = db1_collections - db2_collections
collections_only_in_db2 = db2_collections - db1_collections

print(f"Collections only in {database1_name}:")
for col in collections_only_in_db1:
    print(f"- {col}")

print(f"\nCollections only in {database2_name}:")
for col in collections_only_in_db2:
    print(f"- {col}")

client.close()
