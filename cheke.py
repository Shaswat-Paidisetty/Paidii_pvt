from pymongo import MongoClient

# MongoDB connection details
MONGO_URI = ""mongodb+srv://Paidii:Paidisetty%4010@cluster0.kfocv.mongodb.net/""
DB_NAME = "Dummy"
COLLECTION_NAME = "dummy"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Function to determine field data types
def analyze_field_types():
    field_types = {}

    # Iterate through all documents in the collection
    for doc in collection.find():
        for field, value in doc.items():
            value_type = type(value).__name__
            if field not in field_types:
                field_types[field] = set()
            field_types[field].add(value_type)

    # Print field data types
    for field, types in field_types.items():
        print(f"Field: {field}, Data Types: {', '.join(types)}")

# Run the analysis
analyze_field_types()
