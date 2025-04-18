Here's a simpler version of the `README.md` without smilies:

---

# Doctor Super Clinic Bot

A Python-based chatbot application that helps users book doctor appointments based on their symptoms.

## Features

- Symptom-based doctor suggestions: Based on user input, the chatbot suggests appropriate specialists.
- Doctor list: Users can request a list of available doctors.
- Appointment booking: Users can book appointments with available doctors based on symptoms.

## Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/vpriyankaprabhu/doctor-super-clinic-bot.git
   cd doctor-super-clinic-bot
   ```

2. **Create and activate a virtual environment** (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   Create a `.env` file and add the following:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   If you're using **MongoDB Atlas** (online MongoDB service) instead of a local MongoDB instance, replace the following in your `.env` file:

   ```env
   MONGODB_CONNECTION_STRING=mongodb+srv://<your_username>:<your_password>@cluster0.mongodb.net/<your_database>?retryWrites=true&w=majority
   ```

   Replace `<your_username>`, `<your_password>`, and `<your_database>` with your actual MongoDB Atlas credentials and database name.

   If you're using **MongoDB locally**, the default connection string will be:

   ```env
   MONGODB_CONNECTION_STRING=mongodb://localhost:27017/
   ```

5. **Ensure MongoDB is running**:

   - If using **MongoDB locally**, ensure it's running on your local machine.
   - If using **MongoDB Atlas**, ensure the connection string is correct.

## Running the Application

You have two options to run the bot:

### Option 1: Run `app.py` (with function calling)

```bash
python app.py
```

### Option 2: Run `app-without-functioncalling.py` (without function calling)

```bash
python app-without-functioncalling.py
```

## Example Interaction

### 1. Symptom-based Doctor Suggestions

- **User**: `I have chest pain`
- **Assistant**: Suggests a **Cardiologist**.

  _Example response_:  
  "Based on your symptoms, you should see a Cardiologist. Here are some doctors available in our clinic:  
   1. Dr. Sarah Johnson - Cardiologist - City Hospital  
   2. Dr. Michael Chen - Cardiologist - Mercy Medical Center"

---

### 2. Doctor List

- **User**: `List doctors`
- **Assistant**: Provides a list of available doctors in the database.

  _Example response_:  
  "Here is a list of available doctors:  
   1. Dr. Sarah Johnson - Cardiologist - City Hospital  
   2. Dr. Michael Chen - Dermatologist - Mercy Medical Center  
   3. Dr. Emily Brown - Neurologist - University Hospital  
   4. Dr. James Wilson - Orthopedist - Community Hospital"

---

### 3. Booking Appointment with Doctor

- **User**: `Book appointment with Dr. Emily Brown`
- **Assistant**: Confirms the appointment if the slot is available.

  _Example response_:  
  "Here are available slots for Dr. Emily Brown:  
   1. 2025-04-19 09:00  
   2. 2025-04-20 10:30  
   Please choose a slot and provide your details."

---

### 4. No Available Slots

- **User**: `Book appointment with Dr. John Smith at 5 PM on April 15th`
- **Assistant**: Informs the user if the requested slot is unavailable.

  _Example response_:  
  "Sorry, Dr. John Smith is not available at 5 PM on April 15th. Here are his available slots:  
   1. 2025-04-14 09:00  
   2. 2025-04-14 03:00  
   Please choose another available slot."

---

### 5. Invalid Input

- **User**: `List doctors who can treat a broken arm`
- **Assistant**: Asks for more specific symptoms.

  _Example response_:  
  "Could you please provide more details about your symptoms? A broken arm typically requires attention from an Orthopedist or Emergency Specialist."

---

### 6. Show Available Time Slots

- **User**: `Show timings`
- **Assistant**: Displays available time slots for all doctors.

  _Example response_:  
  "Here is the availability of all doctors:  
   - Dr. Sarah Johnson (Cardiologist): 2025-04-19 10:00, 2025-04-19 14:00  
   - Dr. Michael Chen (Dermatologist): 2025-04-19 11:00, 2025-04-20 13:00  
   - Dr. Emily Brown (Neurologist): 2025-04-19 09:00, 2025-04-20 10:30  
   - Dr. James Wilson (Orthopedist): 2025-04-19 13:30, 2025-04-20 11:00"

---

### 7. Exit Interaction

- **User**: `Exit`
- **Assistant**: Ends the conversation.

  _Example response_:  
  "Thank you for using our service. Take care!"
```