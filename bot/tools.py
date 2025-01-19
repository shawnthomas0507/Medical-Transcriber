import speech_recognition
import pyttsx3
from model import llm
from classes import MessageState
from langchain_core.messages import AIMessage,SystemMessage,HumanMessage
from langgraph.graph import END



engine=pyttsx3.init()
recognizer=speech_recognition.Recognizer()

def record_speech(state: MessageState):
    """
    This tool is used when the doctor wants to take notes.
    """
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

        Remember..do not output any sentence which is not a part of the conversation. Output only the conversation.
        The conversation is as follows: {conversation}
        """
    sys=instructions.format(conversation=recorded_text)
    result=llm.invoke([AIMessage(content=sys)]).content
    return {"formatted_conversation":result.strip()}

def SOAP_formatter(state: MessageState):
    conversation=state["formatted_conversation"]
    print("###")
    print(conversation)
    print("###")
    instructions="""
    You will be provided with  a conversation between a patient and a doctor.
    Your job is to carefully analyse the coversation and summarize it into a SOAP format.
    Do not include and doctor patient conversation, just the SOAP format.

    The SOAP format is as follows along with an example:

    Subjective:  
    - What has the patient been feeling 

    Objective:  
    - Any other symptoms

    Assessment:  
    - The doctor's  Assesment 

    Plan:  
    - What medicines or procedures to take.

    Output only in this format and nothing else. Do not make up any information if any information is missing do not add your own information just say information missing.
    For example if assesment is not provided say information missing.

    The conversation is as follows: {conversation}
    """
    sys=instructions.format(conversation=conversation)
    result=llm.invoke([AIMessage(content=sys)])
    return {"messages":result.content}



def router_condition(state: MessageState):
    soap=state["messages"][-1]
    if "information missing" in soap.content.lower():
        return "reask_node"
    else:
        return "final_node"

def reask(state: MessageState):
    soap=state["messages"][-1].content
    instructions="""
    You will be given the SOAP summary which has the following headings: (Subjective, Objective, Assessment and Plan ).
    Identify which SOAP heading or headings lacks information.
    Create a targeted question to prompt the doctor about the missing information.
    Respond ONLY with the question, starting with "Hey doctor". 

    Example output:
    Hey doctor you have not included the Assesment.

    ### Remember do not add your own information just ask a question!!!
    The SOAP summary is as follows: 
    {summary}  
    """
    sys=instructions.format(summary=soap)
    result=llm.invoke([AIMessage(content=sys)])
    engine.say(result.content)
    engine.runAndWait()
    return {"reask_doctor":result.content}

def general(state: MessageState):
    """
    This tool is used when the doctor asks something general which is not related to taking notes.
    """
    recognizer = speech_recognition.Recognizer()
    engine.say("Yo yo")
    engine.runAndWait()
    return {"messages":"Hi"}

def final_format(state: MessageState):
    final=state["messages"][-1].content
    engine.say(final)
    engine.runAndWait()
    return {"messages":"END"}


def push_mongo(state: MessageState):
    """
    This tool is used when data needs to be pushed to the patient database.
    """
    recognizer = speech_recognition.Recognizer()
    engine.say("I am pushing these clinical notes to the patient database")
    engine.runAndWait()
    ###
    ###
    ###
    #mongo code
    ###
    ###
    engine.say("Data successfully pushed")
    engine.runAndWait()
    return {"messages":"Pushed"}

    
