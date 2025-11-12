from typing import TypedDict, Optional, Dict, Any
from langgraph.graph import StateGraph, END
from app.tools import add_numbers, to_uppercase

# Shared state carried through the graph
class AgentState(TypedDict, total=False):
    user_input: str
    tool_inputs: Dict[str, Any]
    tool_result: Optional[Dict[str, Any]]
    response: Optional[str]
    route: Optional[str]

def node_decide(state: AgentState) -> AgentState:
    """Decide which path to take based on user_input."""
    text = (state.get("user_input") or "").strip().lower()

    # Route to math tool if input asks to add
    import re
    if "add" in text or "+" in text or "sum" in text or "plus" in text:
        nums = [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?", text)]
        if len(nums) >= 2:
            state["tool_inputs"] = {"a": nums[0], "b": nums[1]}
            state["route"] = "math"
            return state

    # Route to uppercase tool if keyword present
    if "uppercase" in text or "upper" in text:
        # naive extraction: everything after 'uppercase'
        state["tool_inputs"] = {"text": state.get("user_input", "")}
        state["route"] = "text"
        return state

    # Default reply
    state["response"] = f"I received: {state.get('user_input', '')}"
    state["route"] = "none"
    return state

def node_math(state: AgentState) -> AgentState:
    """Call add_numbers tool when route is math."""
    if state.get("route") == "math" and state.get("tool_inputs"):
        result = add_numbers(state["tool_inputs"])
        state["tool_result"] = result
        state["response"] = f"Sum is {result['result']}"
    return state

def node_text(state: AgentState) -> AgentState:
    """Call to_uppercase tool when route is text."""
    if state.get("route") == "text" and state.get("tool_inputs"):
        result = to_uppercase(state["tool_inputs"])
        state["tool_result"] = result
        state["response"] = f"Uppercased: {result['result']}"
    return state

def compile_graph():
    """Compile the state graph."""
    g = StateGraph(AgentState)
    g.add_node("decide", node_decide)
    g.add_node("math", node_math)
    g.add_node("text", node_text)

    # Conditional routing from decide
    def route_from_decide(state: AgentState):
        if state.get("route") == "math":
            return "math"
        if state.get("route") == "text":
            return "text"
        return END

    # Use conditional edges from the decide node
    g.add_conditional_edges("decide", route_from_decide)
    g.add_edge("math", END)
    g.add_edge("text", END)
    g.set_entry_point("decide")
    return g.compile()
