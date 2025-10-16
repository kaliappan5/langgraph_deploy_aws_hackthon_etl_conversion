from mcp_schema import MCP
from aws_stub import s3_put, log

PYSPARK_TEMPLATE = """from pyspark.sql import SparkSession, functions as F
spark = SparkSession.builder.getOrCreate()
df = spark.table("{source}")
{body}
df_out.write.mode("overwrite").saveAsTable("{target}")
"""

def dag_to_pyspark(dag):
    code_lines = ["df_out = df"]
    for d in dag:
        if d["step"] == "filter":
            code_lines.append(
                f'df_out = df_out.filter(F.col("{d["column"]}")=="{d["value"]}")')
        if d["step"] == "map":
            code_lines.append(
                f'df_out = df_out.withColumn("{d["column"]}", {d["expr"]})')
        if d["step"] == "select":
            cols = ", ".join(f'"{c}"' for c in d["columns"].split(","))
            code_lines.append(f"df_out = df_out.select({cols})")
    return "\n".join(code_lines)

def converter_node(state: MCP, **_):
    body = dag_to_pyspark(state.dag)
    code = PYSPARK_TEMPLATE.format(
        source="orders_raw",
        body=body,
        target="orders_clean")
    key = f"code/{state.job_id}.py"
    s3_put(key, code)
    log(f"Converter wrote {key}")
    return state.copy(update={
        "code_s3": f"s3://local/{key}",
        "status": "CONVERTED"
    })
