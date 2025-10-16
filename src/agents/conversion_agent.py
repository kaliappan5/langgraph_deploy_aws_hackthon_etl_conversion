import json
from mcp_schema import MCP
from aws_stub import s3_put, log
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import BedrockChat

prompt_template = PromptTemplate.from_template(
    """You are a code generation assistant.

Given the following ETL steps in JSON format, generate equivalent PySpark code.

### Input:
{dag_json}

### Output:
Full PySpark code using DataFrame API."""
)

llm = BedrockChat(model_id="anthropic.claude-3-5-sonnet-20240620-v1:0")  # or claude-3, codewhisperer, etc.

def conversion_node(state: MCP, **_):
    dag_json = json.dumps(state.dag, indent=2)
    prompt = prompt_template.format(dag_json=dag_json)
    
    code = llm.invoke(prompt).content  # ✅ FIXED: Get plain string from AIMessage

    key = f"code/{state.job_id}.py"
    s3_put(key, code)
    log(f"Converter wrote {key}")

    return state.copy(update={
        "code_s3": f"s3://local/{key}",
        "status": "CONVERTED"
    })
