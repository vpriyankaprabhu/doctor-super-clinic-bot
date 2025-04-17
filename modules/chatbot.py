# chatbot.py
import json
from modules.ai_service import generate_chat_response
from modules.appointment_service import find_specialists, get_doctor_availability, book_appointment, list_doctors

def start_chatbot():
    # Set up the system prompt
    messages = [
        {"role": "system", "content": (
            "You are a helpful virtual assistant for a medical clinic. "
            "Help users book appointments with specialists based on their health concerns. "
            "Have a natural, conversational tone. Use the available functions to find specialists, "
            "check availability, and book appointments. Only suggest doctors that are returned by "
            "the functions. Don't invent doctor names or specialties."
        )}
    ]
    
    # Define the functions that OpenAI can call
    functions = [
        {
            "name": "find_specialists",
            "description": "Find appropriate specialists based on patient symptoms",
            "parameters": {
                "type": "object",
                "properties": {
                    "symptoms": {
                        "type": "string",
                        "description": "Description of the patient's symptoms or health concerns"
                    }
                },
                "required": ["symptoms"]
            }
        },
        {
            "name": "get_doctor_availability",
            "description": "Get available appointment slots for a specific doctor",
            "parameters": {
                "type": "object",
                "properties": {
                    "doctor_name": {
                        "type": "string",
                        "description": "The full name of the doctor"
                    }
                },
                "required": ["doctor_name"]
            }
        },
        {
            "name": "book_appointment",
            "description": "Book an appointment with a doctor",
            "parameters": {
                "type": "object",
                "properties": {
                    "doctor_name": {
                        "type": "string",
                        "description": "The full name of the doctor"
                    },
                    "slot": {
                        "type": "string",
                        "description": "The date and time slot for the appointment (format: YYYY-MM-DD HH:MM)"
                    },
                    "patient_name": {
                        "type": "string",
                        "description": "The full name of the patient"
                    },
                    "patient_contact": {
                        "type": "string",
                        "description": "Phone number or email of the patient"
                    }
                },
                "required": ["doctor_name", "slot", "patient_name", "patient_contact"]
            }
        },
        {
            "name": "list_doctors",
            "description": "List all available doctors in the system",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    ]
    
    print("Super Clinic Doctor Appointment Assistant")
    print("==========================================")
    print("Hello and Welcome to the Super Clinic! How can I help you today? You can describe your symptoms or ask to book an appointment.")
    
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        # Check for exit command
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("\nAssistant: Thank you for using our service. Have a great day!")
            break
        
        # Add user message to conversation history
        messages.append({"role": "user", "content": user_input})
        
        try:
            # Get response from OpenAI
            response = generate_chat_response(messages, functions, "auto")
            
            assistant_message = response["choices"][0]["message"]
            
            # Check if a function call is requested
            if "function_call" in assistant_message:
                # Store the assistant's message in history
                messages.append(assistant_message)
                
                # Extract function call details
                function_name = assistant_message["function_call"]["name"]
                function_args = json.loads(assistant_message["function_call"]["arguments"])
                
                # Call the appropriate function
                if function_name == "find_specialists":
                    result = find_specialists(function_args.get("symptoms"))
                    function_response = json.dumps(result)
                
                elif function_name == "get_doctor_availability":
                    result = get_doctor_availability(function_args.get("doctor_name"))
                    function_response = json.dumps(result)
                
                elif function_name == "book_appointment":
                    result = book_appointment(
                        function_args.get("doctor_name"),
                        function_args.get("slot"),
                        function_args.get("patient_name"),
                        function_args.get("patient_contact")
                    )
                    function_response = json.dumps(result)
                
                elif function_name == "list_doctors":
                    result = list_doctors()
                    function_response = json.dumps(result)
                
                # Add the function result to messages
                messages.append({
                    "role": "function",
                    "name": function_name,
                    "content": function_response
                })
                
                # Get a new response that uses the function results
                second_response = generate_chat_response(messages)
                
                # Print the response
                print(f"\nAssistant: {second_response['choices'][0]['message']['content']}")
                
                # Add the final response to the conversation history
                messages.append({"role": "assistant", "content": second_response['choices'][0]['message']['content']})
            
            else:
                # No function call, just print the response
                print(f"\nAssistant: {assistant_message['content']}")
                
                # Add the response to conversation history
                messages.append({"role": "assistant", "content": assistant_message['content']})
                
        except Exception as e:
            print(f"\nAssistant: I'm sorry, I encountered an error: {str(e)}")