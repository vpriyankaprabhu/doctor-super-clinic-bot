# ai_service.py
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client (older style)
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_specialist_recommendation(symptoms):
    """Use OpenAI to recommend a specialist based on symptoms"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a medical expert. Based on the symptoms, suggest a single appropriate medical specialist type."},
            {"role": "user", "content": f"What type of specialist should I see for these symptoms: {symptoms}?"}
        ],
        max_tokens=50
    )
    
    return response["choices"][0]["message"]["content"].strip()

def generate_chat_response(messages, functions=None, function_call=None):
    """Generate a response from the chat model"""
    if functions:
        return openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            functions=functions,
            function_call=function_call
        )
    else:
        return openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )