from pydantic import BaseModel, Field
from typing import Any, Dict, List

class MCP(BaseModel):
    job_id: str
    status: str = "NEW"
    dag: List[Dict[str, Any]] = Field(default_factory=list)
    code_s3: str | None = None
    validation: str | None = None
    hitl_decision: str | None = None
    s3_uri: str