AI Calling Agent

An AI-powered voice interaction system built with Python, Gemini API, Speech-to-Text, Text-to-Speech, FastAPI, and SQLite.

The project simulates inbound and outbound customer calls, understands spoken input, generates intelligent responses, and stores call records for analysis.

🚀 Features

- AI Conversation: Uses Google Gemini API to generate contextual responses.
- Speech-to-Text: Converts spoken audio into text using Faster-Whisper.
- Text-to-Speech: Converts AI responses into spoken audio using pyttsx3.
- Voice Call Simulation: Supports local inbound and outbound call simulations.
- Customer Management: Stores and manages customer records.
- Call Management: Saves call history and conversation details.
- Call Analytics: Tracks call duration, status, and outcomes.
- Data Visualization: Generates visual reports using Matplotlib.
- CSV Reports: Exports call reports for further analysis.
- REST API: Provides backend endpoints using FastAPI.
- API Documentation: Interactive Swagger documentation.

🛠️ Tech Stack

Technology| Purpose
Python| Core programming language
Google Gemini API| AI conversation generation
Faster-Whisper| Speech-to-Text
pyttsx3| Text-to-Speech
FastAPI| Backend API
SQLite| Database
NumPy| Numerical operations
Pandas| Data analysis
Matplotlib| Data visualization
SciPy| Audio processing

📁 Project Structure

AI-Calling-Agent/
│
├── database/
│   └── calls.db
│
├── reports/
│
├── src/
│   ├── database.py
│   ├── customer_manager.py
│   ├── call_manager.py
│   ├── call_analysis.py
│   ├── visualization.py
│   ├── report_generator.py
│   └── call_executor.py
│
├── voice/
│   ├── speech_to_text.py
│   ├── text_to_speech.py
│   ├── gemini_brain.py
│   ├── call_simulator.py
│   └── live_voice_test.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── render.yaml
├── main.py
└── README.md

⚙️ Installation and Setup

1. Clone the repository

git clone https://github.com/nyasharma98-lab/AI-Calling-Agent.git

2. Open the project folder

cd AI-Calling-Agent

3. Create a virtual environment

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

4. Install dependencies

pip install -r requirements.txt

5. Configure Gemini API

Create a ".env" file in the project root.

Add your Gemini API key:

GEMINI_API_KEY=your_gemini_api_key_here

Get an API key from "Google AI Studio" (https://aistudio.google.com/).

Never share or upload your actual API key.

6. Run the FastAPI server

python -m uvicorn main:app --reload

Open the API documentation:

http://127.0.0.1:8000/docs

7. Run the local voice simulator

In a separate terminal:

python -m voice.call_simulator

A working microphone and speaker are required for local voice simulation.

📊 Project Capabilities

The system provides:

- Customer record management
- Inbound and outbound call simulation
- AI-generated conversational responses
- Call history storage
- Call duration analysis
- Call status and outcome tracking
- Data visualization
- CSV report generation
- REST API access

🏗️ Architecture

User Voice Input
       |
       v
Speech-to-Text
       |
       v
Gemini AI
       |
       v
AI Response
       |
       v
Text-to-Speech
       |
       v
Voice Output

       |
       v
Call Management
       |
       v
SQLite Database
       |
       v
Analytics and Reports

🔮 Future Improvements

- Web-based voice interaction interface
- Improved conversation management
- Advanced call analytics
- Persistent cloud database
- Production-ready cloud deployment
- Real telephony integration

⚠️ Project Scope

This project currently focuses on simulated voice calls using local microphone and speaker hardware.

It does not currently place real telephone calls or connect to a telecom provider.

The FastAPI backend can be deployed separately from the local voice simulator.

👩‍💻 Author

Nayasha Sharma

GitHub: "nyasharma98-lab" (https://github.com/nyasharma98-lab)

LinkedIn: "Nayasha Sharma" (https://linkedin.com/in/nayasha-sharma-5b3b8a3b6)

⭐Learn. Build. Improve. Repeat
