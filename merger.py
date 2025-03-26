from pymongo import MongoClient

MONGO_URI = "mongodb+srv://Paidii:Paidisetty%4010@cluster0.kfocv.mongodb.net/"
DB1_NAME = "Dummy"   # Target DB
DB2_NAME = "sample_mflix"      # Source DB

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

def convert_type(value, target_type):
    try:
        if target_type == "int":
            return int(value)
        elif target_type == "float":
            return float(value)
        elif target_type == "str":
            return str(value)
        elif target_type == "bool":
            return bool(value)
        return value
    except:
        return value


def merge_collections():
    for collection in common_collections:
        print(f"\n Merging collection: {collection}")


        schema1 = get_schema(db1, collection)
        schema2 = get_schema(db2, collection)


        keys_db1 = set(schema1.keys())
        keys_db2 = set(schema2.keys())
        missing_in_db2 = keys_db1 - keys_db2
        missing_in_db1 = keys_db2 - keys_db1
        different_types = {key for key in keys_db1 & keys_db2 if schema1[key] != schema2[key]}


        source_docs = list(db2[collection].find({}))

        for doc in source_docs:

            for field in missing_in_db2:
                doc[field] = None


            for field in different_types:
                target_type = schema1[field]
                if field in doc:
                    doc[field] = convert_type(doc[field], target_type)


            db1[collection].update_one({"_id": doc["_id"]}, {"$set": doc}, upsert=True)

        print(f" Merged {len(source_docs)} documents into `{DB1_NAME}.{collection}`")


merge_collections()

client.close()
