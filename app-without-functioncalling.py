import os
import datetime
import openai
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# MongoDB connection
client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING", "mongodb://localhost:27017/"))
db = client["medical_appointments"]
doctors_collection = db["doctors"]
appointments_collection = db["appointments"]

# Initialize database with sample data
def reset_database():
    doctors_collection.drop()
    appointments_collection.drop()

    doctors = [
        {
            "name": "Dr. Sarah Johnson",
            "specialty": "Cardiologist",
            "hospital": "City Hospital",
            "available_slots": ["2025-04-19 10:00", "2025-04-19 14:00", "2025-04-20 09:00"]
        },
        {
            "name": "Dr. Michael Chen",
            "specialty": "Dermatologist",
            "hospital": "Mercy Medical Center",
            "available_slots": ["2025-04-19 11:00", "2025-04-20 13:00", "2025-04-21 15:00"]
        },
        {
            "name": "Dr. Emily Brown",
            "specialty": "Neurologist",
            "hospital": "University Hospital",
            "available_slots": ["2025-04-19 09:00", "2025-04-20 10:30", "2025-04-21 14:00"]
        },
        {
            "name": "Dr. James Wilson",
            "specialty": "Orthopedist",
            "hospital": "Community Hospital",
            "available_slots": ["2025-04-19 13:30", "2025-04-20 11:00", "2025-04-21 10:00"]
        }
    ]

    doctors_collection.insert_many(doctors)
    print("Database initialized with sample doctors.")

# OpenAI to detect specialist

def get_specialist_from_openai(symptoms):
    system_prompt = (
        "You are a medical expert. Based on the symptoms, suggest a single appropriate medical specialist type. "
        "Only reply with the specialty name (like Cardiologist, Dermatologist, Neurologist, etc)."
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"What type of doctor should I see for: {symptoms}?"}
        ],
        max_tokens=50
    )
    return response['choices'][0]['message']['content'].strip()

# Find doctors by specialty
def find_doctors_by_specialty(specialty):
    return list(doctors_collection.find({"specialty": {"$regex": specialty, "$options": "i"}}))

# Get slots for a doctor
def get_doctor_slots(doctor_name):
    doc = doctors_collection.find_one({"name": {"$regex": doctor_name, "$options": "i"}})
    return doc.get("available_slots", []) if doc else []

# Book appointment
def book_appointment(doctor_name, slot, patient_name, patient_contact):
    doctor = doctors_collection.find_one({"name": doctor_name})
    if not doctor or slot not in doctor.get("available_slots", []):
        return {"success": False, "message": "Slot not available."}

    doctors_collection.update_one({"name": doctor_name}, {"$pull": {"available_slots": slot}})

    appointment = {
        "doctor_name": doctor_name,
        "specialty": doctor["specialty"],
        "hospital": doctor["hospital"],
        "appointment_time": slot,
        "patient_name": patient_name,
        "patient_contact": patient_contact,
        "status": "confirmed",
        "created_at": datetime.datetime.now()
    }

    appointments_collection.insert_one(appointment)
    return {"success": True, "message": f"Appointment booked with {doctor_name} on {slot}."}

# CLI Chatbot loop
def chatbot_loop():
    print("Super Clinic Doctor Appointment Assistant")
    print("==========================================")
    print("Hello! Describe your symptoms or directly ask to book an appointment with a specific doctor.")
    print("Type 'exit' to leave the assistant.")

    while True:
        user_input = input("\nYou: ").strip()
        lower_input = user_input.lower()

        if lower_input in ["exit", "quit", "bye"]:
            print("Assistant: Thank you! Take care.")
            break

        try:
            # Show list of all doctors
            if lower_input in ["list doctors", "find doctors", "show doctors"]:
                all_docs = list(doctors_collection.find())
                if not all_docs:
                    print("Assistant: No doctors available at the moment.")
                else:
                    print("Assistant: Here's the list of doctors currently available:")
                    for idx, doc in enumerate(all_docs, 1):
                        print(f"{idx}. {doc['name']} ({doc['specialty']}) - {doc['hospital']}")
                continue

            # Show availability for all doctors
            if any(k in lower_input for k in ["availability", "available", "timings", "slots", "schedule"]):
                all_docs = list(doctors_collection.find())
                if not all_docs:
                    print("Assistant: No doctors available at the moment.")
                else:
                    print("Assistant: Here are available slots for each doctor:\n")
                    for doc in all_docs:
                        print(f"{doc['name']} ({doc['specialty']}) - {doc['hospital']}")
                        slots = doc.get("available_slots", [])
                        if slots:
                            for s in slots:
                                print(f"  - {s}")
                        else:
                            print("  No slots available.")
                        print()
                continue

            # Direct booking attempt (e.g., "book appointment with James")
            if "book" in lower_input and "with" in lower_input:
                parts = user_input.lower().split("with")
                name = parts[1].strip()
                matching_doctor = doctors_collection.find_one({"name": {"$regex": name, "$options": "i"}})
                if not matching_doctor:
                    print("Assistant: Sorry, we couldn't find a doctor with that name.")
                    continue

                slots = get_doctor_slots(matching_doctor["name"])
                if not slots:
                    print("Assistant: No available slots for that doctor.")
                    continue

                print(f"\nAvailable slots for {matching_doctor['name']}:")
                for idx, slot in enumerate(slots, 1):
                    print(f"{idx}. {slot}")
                slot_choice = input("Enter the number of the slot to book (or press Enter to skip): ").strip()
                if slot_choice.isdigit() and 1 <= int(slot_choice) <= len(slots):
                    patient_name = input("Enter your full name: ")
                    patient_contact = input("Enter your phone or email: ")
                    booking = book_appointment(
                        matching_doctor["name"],
                        slots[int(slot_choice)-1],
                        patient_name,
                        patient_contact
                    )
                    print(f"Assistant: {booking['message']}")
                continue

            # Fallback: NLP-based symptom handling
            suggested_specialty = get_specialist_from_openai(user_input)
            doctors = find_doctors_by_specialty(suggested_specialty)

            if not doctors:
                print(f"Assistant: Sorry, we have no {suggested_specialty}s available right now.")
                continue

            print(f"\nAssistant: Based on your symptoms, you should see a {suggested_specialty}.")
            print("Here are available doctors:\n")
            for idx, doc in enumerate(doctors, 1):
                print(f"{idx}. {doc['name']} ({doc['specialty']}) - {doc['hospital']}")

            doctor_choice = input("\nEnter the number of the doctor to see available slots (or press Enter to skip): ").strip()
            if doctor_choice.isdigit() and 1 <= int(doctor_choice) <= len(doctors):
                chosen_doc = doctors[int(doctor_choice)-1]
                slots = get_doctor_slots(chosen_doc["name"])
                if not slots:
                    print("Assistant: No available slots at the moment.")
                    continue
                print("\nAvailable slots:")
                for idx, slot in enumerate(slots, 1):
                    print(f"{idx}. {slot}")
                slot_choice = input("Enter the number of the slot to book (or press Enter to skip): ").strip()
                if slot_choice.isdigit() and 1 <= int(slot_choice) <= len(slots):
                    patient_name = input("Enter your full name: ")
                    patient_contact = input("Enter your phone or email: ")
                    booking = book_appointment(
                        chosen_doc["name"],
                        slots[int(slot_choice)-1],
                        patient_name,
                        patient_contact
                    )
                    print(f"Assistant: {booking['message']}")

        except Exception as e:
            print(f"Assistant: Oops! Something went wrong. Error: {str(e)}")

if __name__ == "__main__":
    reset_database()
    chatbot_loop()