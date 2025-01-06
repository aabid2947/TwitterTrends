from pymongo import MongoClient
import os 
from dotenv import load_dotenv
import datetime
import random
import string
# Load environment variables
load_dotenv()

# Load credentials and MongoDB URI

MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME')

# Create a function to generate a unique ID for each run
def generate_unique_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


# Create a function to store the trends in MongoDB
def store_trends_in_db(trends, ip_address):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db['trending_topics']
    
    # Fill missing trends with placeholders if fewer than 5 are found
    while len(trends) < 5:
        trends.append('No data available')

    unique_id = generate_unique_id()
    
    record = {
        'unique_id': unique_id,
        'trend': trends,
        'date_time': datetime.now(),
        'ip_address': ip_address
    }
    print(record)

    collection.insert_one(record)
    client.close()

def view_trending_topics():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db['trending_topics']
    
    # Fetch all records
    records = collection.find()
    for record in records:
        print(record)
    
    client.close()
# Function to fetch the latest entry from the database
def fetch_latest_entry_from_db():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db['trending_topics']
    
    # Fetch the latest entry by sorting based on 'date_time' in descending order
    latest_entry = collection.find_one({}, sort=[('date_time', -1)])

    client.close()

    if latest_entry:
        # Return the latest entry (exclude '_id' if you don't want to send it back to the client)
        latest_entry.pop('_id', None)
        
        return latest_entry
    else:
        return {'error': 'No trends data found in database'}

def clear_all_data():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db['trending_topics']  # Specify the collection name
    
    # Delete all documents in the collection
    collection.delete_many({})
    
    print("All data has been deleted.")
    
    client.close()


