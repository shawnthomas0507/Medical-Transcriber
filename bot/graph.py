from langgraph.graph import START,END,StateGraph
from classes import MessageState
from tools import SOAP_formatter,record_speech,format_conversation,reask,router_condition,general,final_format,push_mongo,record_intro_speech
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from model import llm
from langgraph.prebuilt import ToolNode,tools_condition
from IPython.display import Image,display

llm_with_tools=llm.bind_tools(tools=[record_speech,general,push_mongo])


def router_agent(state: MessageState):
    tool_call=llm_with_tools.invoke(state["messages"])
    return tool_call.additional_kwargs['tool_calls'][0]['function']['name']



graph=StateGraph(MessageState)
graph.add_node("record_intro_speech",record_intro_speech)
graph.add_node("record_speech",record_speech)
graph.add_node("push_mongo",push_mongo)
graph.add_node("format_conversation",format_conversation)
graph.add_node("SOAP_formatter",SOAP_formatter)
graph.add_node("reask_node",reask)
graph.add_node("general",general)
graph.add_node("final_node",final_format)
graph.add_edge(START,"record_intro_speech")
graph.add_conditional_edges("record_intro_speech",router_agent,["record_speech","general","push_mongo"])
graph.add_edge("general","record_intro_speech")
graph.add_edge("push_mongo","record_intro_speech")
graph.add_edge("record_speech","format_conversation")
graph.add_edge("format_conversation","SOAP_formatter")
graph.add_conditional_edges("SOAP_formatter",router_condition,["final_node","reask_node"])
graph.add_edge("final_node","record_intro_speech")
graph.add_edge("reask_node","record_speech")
memory=MemorySaver()
app=graph.compile(checkpointer=memory)
display(Image(app.get_graph().draw_mermaid_png()))







