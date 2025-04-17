# app.py
import os
from dotenv import load_dotenv
from modules.database import setup_database
from modules.chatbot import start_chatbot

# Load environment variables
load_dotenv()

def main():
    # Setup database
    setup_database()
    
    # Start chatbot
    start_chatbot()

if __name__ == "__main__":
    main()