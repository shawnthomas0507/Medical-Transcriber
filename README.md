# Medical Transcriber

## Overview

The Medical Transcriber is an AI-powered application designed to assist healthcare professionals in transcribing and managing patient interactions. Utilizing advanced speech recognition and natural language processing technologies, this tool aims to streamline the documentation process, allowing doctors to focus more on patient care.

## Features

- **Speech Recognition**: Converts spoken language into text, enabling doctors to dictate notes seamlessly.
- **SOAP Note Generation**: Automatically formats transcribed conversations into the SOAP (Subjective, Objective, Assessment, Plan) format for easy documentation.
- **Medication Call Scripts**: Generates professional call scripts for pharmacies based on clinical notes.
- **Interactive Voice Response**: Engages with users through voice prompts and responses, enhancing user experience.
- **MongoDB Integration**: Stores clinical notes and patient data securely in a MongoDB database.

## Technologies Used

- **Python**: The primary programming language for backend development.
- **Twilio**: For making voice calls and sending messages.
- **SpeechRecognition**: For converting speech to text.
- **Pyttsx3**: For text-to-speech conversion.
- **LangChain**: For managing conversational AI and message handling.
- **MongoDB**: For data storage and retrieval.

## Installation

To set up the Medical Transcriber on your local machine, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Medical-Transcriber.git
   cd Medical-Transcriber/bot
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Create a `.env` file in the `bot` directory and add your Twilio credentials and any other necessary API keys.

5. **Run the application**:
   ```bash
   python main.py
   ```

## Usage

1. **Start the application**: Run the `main.py` file to initiate the Medical Transcriber.
2. **Interact with the application**: Use voice commands to dictate notes or ask questions. The application will respond accordingly.
3. **Access stored data**: Clinical notes and patient data can be accessed through your own MongoDB database.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.


  To be continued....
