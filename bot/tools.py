import speech_recognition
import pyttsx3
from model import llm
from classes import MessageState
from langchain_core.messages import AIMessage,SystemMessage,HumanMessage
from langgraph.graph import END
from mongo import client


engine=pyttsx3.init()
recognizer=speech_recognition.Recognizer()

def record_speech(state: MessageState):
    """
    This tool is used when the doctor wants to take notes. Only if he says anything about notes then only call this tool.
    """
    recognizer = speech_recognition.Recognizer()
    engine.say("Hey Doctor. I have started taking notes")
    engine.runAndWait()

    final = ""
    
    while True:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.1)
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
    
    return {"recorded_text":final.strip(),"spoken_messages":""}

def format_conversation(state: MessageState):
    recorded_text=state["recorded_text"]
    instructions="""
        Label each sentence in the following conversation as either "Patient" or "Doctor." Output each labeled sentence in the format:
        [Speaker]: [Sentence] 

        Just give me the labelled conversation.
        The conversation is as follows: {conversation}  
    """
    sys=instructions.format(conversation=recorded_text)
    result=llm.invoke([AIMessage(content=sys)]).content
    return {"formatted_conversation":result,"spoken_messages":""}

def SOAP_formatter(state: MessageState):
    conversation=state["formatted_conversation"]
    db=client['patient']
    vitals=db['patient_vitals']
    vital=vitals.find_one({"patient_id":1})
    instructions="""
    You will be provided with a conversation between a patient and a doctor and the vitals of the patient.
    Your task is to **extract** information from the conversation and summarize it in the **SOAP format** without adding any extra information.  

    ### **Instructions:**  
    1. **Do not** modify, interpret, or add any extra details.  
    2. **Only use** the information present in the conversation.  
    3. If any section (Subjective, Objective, Assessment, or Plan) is missing, state **"Information missing."**  
    4. Output must be **strictly** in the following format:  

    
    Clinical Notes:  

    Subjective:  
    - [Extracted details from conversation]  

    Objective:  
    - [Extracted details from conversation]  

    Assessment:  
    - [Extracted details from conversation or state "Information missing."]  

    Plan:  
    - [Extracted details from conversation or state "Information missing."]  

    ### **Conversation:**  
    {conversation}  

    ### **Vitals:**
    {vitals}

    **Output only in the above format. Do not add explanations, interpretations, or extra details.**  

    """
    sys=instructions.format(conversation=conversation,vitals=vital['vitals'])
    result=llm.invoke([AIMessage(content=sys)])
    return {"messages":result.content,"spoken_messages":""}



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
    return {"reask_doctor":result.content,"spoken_messages":result.content}

def general(state: MessageState):
    """
    This tool is used when the doctor asks something general which is not related to taking notes.
    Like what medicines did i mention and so on. Any general queestion.
    """
    try:
        soap_info = state["soap"]
    except KeyError:
        soap_info = None  

    query = state["messages"][-1].content

    if soap_info:

        instructions="""
        You will be provided with a SOAP summary {summary}.
        Using this context answer the question the user may have.
        Even if the user asks a question outside the context answer it.

        The user's question is {question}
        {summary}  
        """
        sys=instructions.format(question=query,summary=soap_info)
        
        recognizer = speech_recognition.Recognizer()
        result=llm.invoke([AIMessage(content=sys)])
        engine.say(result.content)
        engine.runAndWait()
        return {"messages":result.content,"spoken_messages":result.content}
    
    else:
        instructions="""
        "You are Sofia, a world class Medical Scribe".
        You have to give a proper formal answer based on the user's question.
        The user's question is {question}
        """
        sys=instructions.format(question=query)
        
        recognizer = speech_recognition.Recognizer()
        result=llm.invoke([AIMessage(content=sys)])
        engine.say(result.content)
        engine.runAndWait()
        return {"messages":result.content,"spoken_messages":result.content}


def final_format(state: MessageState):
    final=state["messages"][-1].content
    return {"messages":"END","soap":final,"spoken_messages":final}


def push_mongo(state: MessageState):
    """
    This tool is used when data needs to be pushed to the patient database.
    """
    clinical=state["soap"]
    db=client['patient']
    notes=db['clinical_notes']
    notes.insert_one({'notes':clinical})
    return {"messages":"Pushed","spoken_messages":"Data successfully pushed"}

    
def record_intro_speech(state: MessageState):
    
    recognizer = speech_recognition.Recognizer()
    engine = pyttsx3.init()
    final = ""
    
    
    while True:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.1)
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
    
    return {"messages":final.strip(),"spoken_messages":""}


def exit(state: MessageState):
    """
        This tool is triggered when the user expresses gratitude, or intends to exit.  
    """
    return {"messages":"Glad I could help See you soon","spoken_messages":"Glad I could help See you soon"}


