# appointment_service.py
import datetime
from modules.database import doctors_collection, appointments_collection
from modules.ai_service import get_specialist_recommendation

# Functionality to find specialists, check availability, and book appointments
def find_specialists(symptoms):
    suggested_specialty = get_specialist_recommendation(symptoms)
    
    # Find doctors with the suggested specialty
    doctors = list(doctors_collection.find({"specialty": suggested_specialty}))
    
    # If no exact match, try to find similar specialties
    if not doctors:
        for doctor in doctors_collection.find():
            if suggested_specialty.lower() in doctor["specialty"].lower():
                doctors.append(doctor)
    
    return {
        "suggested_specialty": suggested_specialty,
        "doctors": [{"name": doc["name"], "specialty": doc["specialty"], "hospital": doc["hospital"]} for doc in doctors]
    }

# Get available appointment slots for a specific doctor
def get_doctor_availability(doctor_name):
    doctor = doctors_collection.find_one({"name": doctor_name})
    if doctor and "available_slots" in doctor:
        return {"slots": doctor["available_slots"]}
    return {"slots": []}

# Book an appointment with a doctor
def book_appointment(doctor_name, slot, patient_name, patient_contact):
    # Check if doctor and slot exist
    doctor = doctors_collection.find_one({"name": doctor_name})
    if not doctor or slot not in doctor.get("available_slots", []):
        return {"success": False, "message": "This appointment slot is not available"}
    
    # Remove the slot from available slots
    doctors_collection.update_one(
        {"name": doctor_name},
        {"$pull": {"available_slots": slot}}
    )
    
    # Create appointment record
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
    
    result = appointments_collection.insert_one(appointment)
    
    return {
        "success": True,
        "appointment_id": str(result.inserted_id),
        "message": f"Appointment confirmed with {doctor_name} on {slot}"
    }

def list_doctors():
    """List all available doctors in the system"""
    doctors = list(doctors_collection.find({}, {"name": 1, "specialty": 1, "hospital": 1, "_id": 0}))
    return {"doctors": doctors}