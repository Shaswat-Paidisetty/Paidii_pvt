from flask import Flask, render_template, request, redirect, url_for
import pymongo
import os
from bson import ObjectId

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://Paidii:Paidisetty%4010@cluster0.kfocv.mongodb.net/")
db = client["Dummy"]
collection = db["dummy collection"]

OFFSET_FILE = r"C:\Users\Admin\PyCharmMiscProject\New counter\offset_id.txt"
last_fetched_id = None

def get_last_id():
    global last_fetched_id
    if os.path.exists(OFFSET_FILE):
        with open(OFFSET_FILE, "r") as file:
            last_fetched_id = file.read().strip()
    else:
        last_fetched_id = None

def save_last_id():
    global last_fetched_id
    if last_fetched_id:
        with open(OFFSET_FILE, "w") as file:
            file.write(str(last_fetched_id))

def fetch_next_data(limit=100, force_default=False):
    global last_fetched_id
    query = {}

    if last_fetched_id and not force_default:
        query = {"_id": {"$gt": ObjectId(last_fetched_id)}}

    entries = collection.find(query).sort("_id", pymongo.ASCENDING).limit(limit)
    entry_list = list(entries)

    if entry_list:
        last_fetched_id = entry_list[-1]['_id']
        save_last_id()
    return entry_list

def fetch_previous_data(limit=100):
    global last_fetched_id

    if last_fetched_id is None:
        return []

    query = {"_id": {"$lt": ObjectId(last_fetched_id)}}
    entries = collection.find(query).sort("_id", pymongo.DESCENDING).limit(limit)
    entry_list = list(entries)

    if entry_list:
        last_fetched_id = entry_list[-1]['_id']
        save_last_id()
    return entry_list

@app.route('/', methods=['GET', 'POST'])
def index():
    global last_fetched_id
    get_last_id()

    if request.method == 'POST':
        action = request.form.get('action')
        limit = int(request.form.get('limit', 100))

        if action == 'next':
            entries = fetch_next_data(limit, force_default=(last_fetched_id is None))
        elif action == 'previous':
            entries = fetch_previous_data(limit)
        else:
            entries = []

        return render_template('index.html', entries=entries, last_fetched_id=last_fetched_id)

    return render_template('index.html', entries=[], last_fetched_id=last_fetched_id)

if __name__ == '__main__':
    app.run(debug=True)