from typing import TypedDict,Sequence
from typing import Annotated
from langchain_core.messages import BaseMessage,SystemMessage,HumanMessage
from langgraph.graph.message import add_messages
from operator import add



class MessageState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]
    recorded_text: Annotated[str,add]
    reask_doctor: str
    formatted_conversation: Annotated[str,add]
    soap: str