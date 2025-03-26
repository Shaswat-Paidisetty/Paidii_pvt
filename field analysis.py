from pymongo import MongoClient
from collections import defaultdict
import inflect

MONGO_URI = "mongodb+srv://prod_read_access_user:LQFtkbsod9d9wuyk@elabsproduction.lagpo.mongodb.net/?retryWrites=true&w=majority&appName=ElabsProduction"
DATABASE_NAME = "itclabs-prod"
COLLECTION_NAME = "el_orders"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]


def find_similar_field_names(fields):
    p = inflect.engine()
    singular_to_plural = defaultdict(list)

    for field in fields:
        singular_form = p.singular_noun(field)
        if singular_form:
            singular_to_plural[singular_form].append(field)
        else:
            singular_to_plural[field].append(field)

    similar_fields = {key: values for key, values in singular_to_plural.items() if len(values) > 1}
    return similar_fields


all_fields_pipeline = [
    {"$project": {"fields": {"$objectToArray": "$$ROOT"}}},
    {"$unwind": "$fields"},
    {"$group": {"_id": "$fields.k"}}
]

all_fields = [r["_id"] for r in collection.aggregate(all_fields_pipeline)]

similar_fields = find_similar_field_names(all_fields)

empty_fields = {}
for singular, variants in similar_fields.items():
    for field in variants:
        if collection.count_documents(
                {field: {"$exists": True, "$ne": None, "$not": {"$type": "array"}, "$not": {"$type": "object"}}}) == 0:
            empty_fields[field] = "Empty"

total_docs = collection.estimated_document_count()
threshold = 0.001 * total_docs

pipeline = [
    {"$project": {"fields": {"$objectToArray": "$$ROOT"}}},
    {"$unwind": "$fields"},
    {"$group": {"_id": "$fields.k", "total_occurrences": {"$sum": 1}}},
    {"$match": {"total_occurrences": {"$lt": threshold}}},
    {"$project": {"field": "$_id", "_id": 0}},
]

irrelevant_fields = [r["field"] for r in collection.aggregate(pipeline)]

print("Irrelevant Fields (appear in <1% of documents):", irrelevant_fields)
print("Similar Fields (singular/plural forms detected):", similar_fields)
print("Empty Fields within Similar Groups:", empty_fields)

client.close()