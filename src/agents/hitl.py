from mcp_schema import MCP

def hitl_node(state: MCP, **_):
    # Example: auto-approve
    return state.copy(update={
        "hitl_decision": "APPROVE",
        "status": "APPROVED"
    })
