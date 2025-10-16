import boto3

s3 = boto3.client("s3")

def s3_get(s3_uri: str) -> str:
    if not s3_uri.startswith("s3://"):
        raise ValueError("Invalid S3 URI")
    s3_path = s3_uri.replace("s3://", "")
    bucket, key = s3_path.split("/", 1)
    response = s3.get_object(Bucket=bucket, Key=key)
    return response["Body"].read().decode("utf-8")

def s3_put(key: str, content: str, bucket: str = "fs-etl-output"):
    s3.put_object(Body=content.encode("utf-8"), Bucket=bucket, Key=key)

def log(message: str):
    print(f"[LOG] {message}")
