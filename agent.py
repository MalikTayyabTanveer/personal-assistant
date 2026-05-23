from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AIMessageChunk
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from IPython.display import Image
from langchain_core.messages import HumanMessage
from pydantic_models.agentstate import AgentState
from agent_component.agent_node import llm_node
from agent_component.conditional_node import should_search
from agent_component.tool_node import web_search

TOOLS = [web_search]
checkpointer = MemorySaver()

# define graph with state and compile
workflow = StateGraph(AgentState)
workflow.add_node("llm", llm_node)
workflow.add_node("web_search", ToolNode(TOOLS))


workflow.add_edge(START, "llm")
workflow.add_conditional_edges(
    "llm",
    should_search,
    {
        "tools": "web_search",
        "end": END
    }
)
workflow.add_edge("web_search", "llm")
graph = workflow.compile(checkpointer=checkpointer)

config = {
        "configurable": {"thread_id": 1},
        "recursion_limit": 10
    }
# Query the graph
try:
    while True:
        user_input = input("Your message: ")
        if user_input.lower() in ["exit", "quit", "bye","goodbye"]:
            break
        for result, metadata in graph.stream(config=config, input={"messages": [HumanMessage(content=user_input)]}, stream_mode="messages"):
            if isinstance(result, AIMessageChunk) and result.content:
                print(result.content, end="", flush=True)
        print("")
except KeyboardInterrupt:
    print("\nExiting the chat. Goodbye!")