# Medical AI Transcriber

This project is a **Medical AI Transcriber** designed to convert spoken language into clinical notes. The transcriber processes real-time voice input and generates formatted clinical notes using the **SOAP** (Subjective, Objective, Assessment, Plan) format. The system integrates AI-powered tools to transcribe, format, and store the notes in a MongoDB database.

## Features

- **Real-Time Voice Transcription**: The system listens to the user’s speech and transcribes it in real-time.
- **SOAP Formatter**: Converts transcribed speech into structured clinical notes using the SOAP format.
- **MongoDB Integration**: The transcriptions are pushed to a MongoDB database for storage.
- **AI Agent Integration**: Uses AI tools to determine the appropriate processing flow.
- **Intuitive Interface**: Provides a user-friendly interface for seamless interaction and voice recording.

## Installation

### Prerequisites

- Python 3.x
- MongoDB or another database for storing clinical notes (optional)
- Required Python packages (`requirements.txt`)

### Steps to Install

1. Clone the repository:
   git clone https://github.com/yourusername/medical-ai-transcriber.git

2. Navigate to project directory
3. Install the dependencies
   pip install -r requirements.txt
