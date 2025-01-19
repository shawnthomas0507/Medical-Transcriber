from graph import app
from langchain_core.messages import HumanMessage, AIMessage,SystemMessage
import speech_recognition
import pyttsx3
import os

os.environ["GROQ_API_KEY"] = ""

recognizer=speech_recognition.Recognizer()
engine=pyttsx3.init()


def record_speech():
    
    recognizer = speech_recognition.Recognizer()
    engine = pyttsx3.init()
    final = ""
    
    engine.say("Hey Doctor. How can I help")
    engine.runAndWait()
    
    while True:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                print("Listening....")
                audio = recognizer.listen(mic, timeout=3, phrase_time_limit=None)
                
                text = recognizer.recognize_groq(audio)
                text = text.lower()
                
                if "stop recording" in text:
                    print("Stopping recording...")
                    break
                    
                final += " " + text
                print(text)
                
        except speech_recognition.WaitTimeoutError:
            print("No speech detected for 3 seconds. Stopping recording...")
            break
            
        except speech_recognition.UnknownValueError:
            print("Could not understand audio. Stopping recording...")
            break
            
        except Exception as e:
            print(f"Error occurred: {e}")
            break
    
    return final.strip()


starting=record_speech()
thread={"configurable":{"thread_id":"1"}}
for event in app.stream({"messages": [HumanMessage(content=starting)]},thread,stream_mode="values"):
    event["messages"][-1].pretty_print()