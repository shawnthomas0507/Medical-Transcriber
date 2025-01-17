from typing import TypedDict,Sequence
from typing import Annotated
from langchain_core.messages import BaseMessage,SystemMessage,HumanMessage
from langgraph.graph.message import add_messages


class MessageState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]
    recorded_text: Annotated[list[BaseMessage],add_messages]
    reask_doctor: str
    formatted_conversation: Annotated[list[BaseMessage],add_messages]