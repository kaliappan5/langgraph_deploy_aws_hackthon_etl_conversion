from mcp_schema import MCP
from aws_stub import log

def validator_node(state: MCP, **_):
    # Stub always passes
    log("Validator PASS")
    return state.copy(update={
        "validation": "PASS",
        "status": "VALIDATED"
    })
