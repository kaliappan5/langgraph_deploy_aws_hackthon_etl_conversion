import xmltodict, uuid
from mcp_schema import MCP
from aws_stub import s3_get, log

def analyzer_node(state: MCP, **_):
    s3_uri = state.s3_uri
    if not s3_uri:
        raise ValueError("s3_uri must be set in the state!")
    body = s3_get(s3_uri)
    job_dict = xmltodict.parse(body)["job"]
    dag = []
    # Fix: Support both list and dict for steps
    steps = job_dict["steps"]["step"]
    if isinstance(steps, list):
        for step in steps:
            dag.append(dict(step))
    else:
        dag.append(dict(steps))
    new = state.copy(update={
        "status": "ANALYZED",
        "dag": dag
    })
    log(f"Analyzer OK for {state.job_id}")
    return new