# database.py

import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to MongoDB
mongo_client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING", "mongodb://localhost:27017/"))
db = mongo_client["medical_appointments"]
doctors_collection = db["doctors"]
appointments_collection = db["appointments"]

# Function to drop existing collections and Initialize database with sample doctors data
def setup_database():
    # Clear existing data
    doctors_collection.drop()
    appointments_collection.drop()
    
    # Insert sample doctors
    doctors = [
        {
            "name": "Dr. Sarah Johnson",
            "specialty": "Cardiologist",
            "hospital": "City Hospital",
            "available_slots": [
                "2025-04-14 10:00", "2025-04-14 14:00", "2025-04-15 09:00"
            ]
        },
        {
            "name": "Dr. Michael Chen",
            "specialty": "Dermatologist",
            "hospital": "Mercy Medical Center",
            "available_slots": [
                "2025-04-14 11:00", "2025-04-15 13:00", "2025-04-16 15:00"
            ]
        },
        {
            "name": "Dr. Emily Brown",
            "specialty": "Neurologist", 
            "hospital": "University Hospital",
            "available_slots": [
                "2025-04-14 09:00", "2025-04-15 10:30", "2025-04-16 14:00"
            ]
        },
        {
            "name": "Dr. James Wilson",
            "specialty": "Orthopedist",
            "hospital": "Community Hospital",
            "available_slots": [
                "2025-04-14 13:30", "2025-04-15 11:00", "2025-04-16 10:00"
            ]
        }
    ]
    
    doctors_collection.insert_many(doctors)
    print("Database initialized with sample doctors")