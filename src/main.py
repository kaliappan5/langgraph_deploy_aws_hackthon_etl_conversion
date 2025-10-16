from mcp_schema import MCP
from graph import build_graph
from aws_stub import s3_put

def main():
    # Upload the test XML to the stub S3
    with open("test_job.xml") as f:
        s3_put("test_job.xml", f.read())

    # Build initial state
    state = MCP(
        job_id="test-job-001",
        status="NEW",
        s3_uri="test_job.xml"
    )
    g = build_graph(hitl=True)
    result = g.invoke(state)
    print(result)

if __name__ == "__main__":
    main()