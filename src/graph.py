from langgraph.graph import StateGraph, START, END
from mcp_schema import MCP
from agents.analyzer import analyzer_node
from agents.conversion_agent import conversion_node  # Claude-powered
from agents.validator import validator_node
from agents.hitl import hitl_node

def build_graph(hitl: bool = True) -> StateGraph:
    g = StateGraph(state_schema=MCP)
    g.add_node("analyzer", analyzer_node)
    g.add_node("converter", conversion_node)
    g.add_node("validator", validator_node)
    g.add_node("hitl", hitl_node)

    g.add_edge(START, "analyzer")
    g.add_edge("analyzer", "converter")
    g.add_edge("converter", "validator")

    if hitl:
        g.add_edge("validator", "hitl")
        g.add_edge("hitl", END)
    else:
        g.add_edge("validator", END)

    return g.compile()