from pymongo import MongoClient

MONGO_URI = ""mongodb+srv://Paidii:Paidisetty%4010@cluster0.kfocv.mongodb.net/""

DB1_NAME = "Dummy"
DB2_NAME = "Dummy_1"

client = MongoClient(MONGO_URI, connect=False)
db1 = client[DB1_NAME]
db2 = client[DB2_NAME]

collections_db1 = set(db1.list_collection_names())
collections_db2 = set(db2.list_collection_names())

common_collections = collections_db1 & collections_db2

def get_schema(db, collection_name):
    sample_doc = db[collection_name].find_one()
    if not sample_doc:
        return {}
    return {key: type(value).__name__ for key, value in sample_doc.items()}

for collection in common_collections:
    schema1 = get_schema(db1, collection)
    schema2 = get_schema(db2, collection)

    print(f"\n Comparing schema for collection: {collection}")

    keys_db1 = set(schema1.keys())
    keys_db2 = set(schema2.keys())

    missing_in_db2 = keys_db1 - keys_db2
    missing_in_db1 = keys_db2 - keys_db1

    different_types = {key for key in keys_db1 & keys_db2 if schema1[key] != schema2[key]}

    if missing_in_db2:
        print(f" Fields in `{DB1_NAME}` but missing in `{DB2_NAME}`: {missing_in_db2}")
    if missing_in_db1:
        print(f" Fields in `{DB2_NAME}` but missing in `{DB1_NAME}`: {missing_in_db1}")
    if different_types:
        print(f" Fields with different types:")
        for field in different_types:
            print(f"  - `{field}`: {DB1_NAME} → {schema1[field]}, {DB2_NAME} → {schema2[field]}")

client.close()
