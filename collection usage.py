from pymongo import MongoClient

# MongoDB connection setup
client = MongoClient("mongodb+srv://prod_read_access_user:LQFtkbsod9d9wuyk@elabsproduction.lagpo.mongodb.net/?retryWrites=true&w=majority&appName=ElabsProduction")
db = client["itclabs-prod"]
collection = db["el_parameter_category"]

# Fetch all documents from the collection
total_documents = collection.count_documents({})

# Dictionary to store field usage counts
field_usage = {}

# Iterate through documents to count field occurrences
for doc in collection.find():
    for field in doc:
        if field != "_id":  # Ignore MongoDB default _id field
            field_usage[field] = field_usage.get(field, 0) + 1

# Calculate and display usage percentage for each field
print("Field usage in collection 'el_category':")
for field, count in field_usage.items():
    usage_percentage = (count / total_documents) * 100 if total_documents > 0 else 0
    print(f"{field}: {usage_percentage:.2f}%")
