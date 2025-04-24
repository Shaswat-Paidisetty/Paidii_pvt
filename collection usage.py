from pymongo import MongoClient

# MongoDB connection setup
client = MongoClient(""mongodb+srv://Paidii:Paidisetty%4010@cluster0.kfocv.mongodb.net/""]
collection = db["Dummy"]

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
print("Field usage in collection 'Dummy':")
for field, count in field_usage.items():
    usage_percentage = (count / total_documents) * 100 if total_documents > 0 else 0
    print(f"{field}: {usage_percentage:.2f}%")
