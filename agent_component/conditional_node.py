from pydantic_models.agentstate import AgentState


def should_search(state: AgentState):

    if not state['messages']:
        return "end"
    
    last_message = state['messages'][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    return "end"