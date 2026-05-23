import os
import time
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, AIMessage
from pydantic_models.agentstate import AgentState
from agent_component.tool_node import web_search
from prompt.prompt_reader import read_prompt

load_dotenv()
formatted_time = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())


PROMPT = read_prompt().format(DATETIME = formatted_time)
LLM_WITH_TOOL = None
MODEL = None


def init_llm():
    global LLM_WITH_TOOL, MODEL

    if LLM_WITH_TOOL is not None and MODEL is not None:
        return
    
    MODEL = os.getenv("model")
    if not MODEL or "" == MODEL:
        print("define your model path in env folder")
    groq_api_key = os.getenv("groq_api_key")
    llm = ChatGroq(
        api_key=groq_api_key,
        model=MODEL,
        temperature= 0.3
    )
    LLM_WITH_TOOL = llm.bind_tools([web_search])


def llm_node(state: AgentState):

    init_llm()
    messages = [SystemMessage(content=PROMPT)] + state["messages"]

    result = LLM_WITH_TOOL.invoke(messages)

    return {"messages": [result]}

