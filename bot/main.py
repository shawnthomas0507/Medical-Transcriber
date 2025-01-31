from graph import app
from langchain_core.messages import HumanMessage, AIMessage,SystemMessage
import speech_recognition
import pyttsx3
import os

os.environ["GROQ_API_KEY"] = ""

recognizer=speech_recognition.Recognizer()
engine=pyttsx3.init()

engine.say("Hey doctor how can i help?")
engine.runAndWait()
thread={"configurable":{"thread_id":"1"}}
for event in app.stream({"messages": [HumanMessage(content="Hi")]},thread,stream_mode="values"):
    event["messages"][-1].pretty_print()

