import speech_recognition
import pyttsx3
from model import llm
from classes import MessageState
from langchain_core.messages import AIMessage,SystemMessage,HumanMessage
from langgraph.graph import END



engine=pyttsx3.init()
recognizer=speech_recognition.Recognizer()

def record_speech(state: MessageState):
    recognizer = speech_recognition.Recognizer()
    engine.say("Hey Doctor. I have started recording")
    engine.runAndWait()

    final = ""
    
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
    
    return {"recorded_text":final.strip()}

def format_conversation(state: MessageState):
    recorded_text=state["recorded_text"]
    instructions="""
    You will be provided with a conversation between a patient and doctor.
    Your job is to label each conversation as doctor or patient.
    Remember, do not make up or put your own information in this.
    Carefully analyze each sentence.

    For example:
    Input: How have you been feeling today
    Output: Doctor: How have you been feeling today

    The conversation is as follows: {conversation}
    """
    sys=instructions.format(conversation=recorded_text)
    result=llm.invoke([AIMessage(content=sys)]).content
    return {"formatted_conversation":result}

def SOAP_formatter(state: MessageState):
    conversation=state["formatted_conversation"]
    instructions="""
    You will be provided with  a conversation between a patient and a doctor.
    Your job is to carefully analyse the coversation and summarize it into a SOAP format.

    The SOAP format is as follows along with an example:

    Subjective:  
    - What has the patient been feeling 

    Objective:  
    - Any other symptoms

    Assessment:  
    - The doctor's  Assesment 

    Plan:  
    - What medicines or procedures to take.

    Output only in this format and nothing else. Do not make up any information if any information is missing do not add your own information just say information not provided.
    For example if assesment is not provided say information not provided.

    The conversation is as follows: {conversation}
    """
    sys=instructions.format(conversation=conversation)
    result=llm.invoke([AIMessage(content=sys)])
    return {"messages":result.content}



def router_condition(state: MessageState):
    soap=state["messages"][-1]
    if "information not provided    " in soap.content.lower():
        return "reask_node"
    else:
        return "final_node"

def reask(state: MessageState):
    soap=state["messages"][-1].content
    instructions="""
    You will be given the SOAP summary of a conversation between a doctor and patient.
    You will find out under what heading is information not provided.
    Using that heading create a question to prompt the doctor that he/she has not provided the specific information.
    Just give me the question nothing else. 
    Remember clearly!!! Do not add anything else. Always start with Hey doctor.
    For example:
    Hey doctor you have not included the plan. 

    The summary is as follows: {summary}  
    """
    sys=instructions.format(summary=soap)
    result=llm.invoke([AIMessage(content=sys)])
    engine.say(result.content)
    engine.runAndWait()
    return {"reask_doctor":result.content}

def multiply(a: int,b: int):
    """Multiply a and b.

    Args:
    a: first int
    b: second int
    """
    return "Hi"

def final_format(state: MessageState):
    final=state["messages"][-1].content
    engine.say(final)
    engine.runAndWait()
    return {"messages":"END"}


