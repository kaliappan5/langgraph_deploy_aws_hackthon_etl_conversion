import os
import boto3
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_openai import AzureChatOpenAI
from chat_agent.utils.state import State
from langchain_aws import ChatBedrockConverse


_ = load_dotenv()

# 1. Initialize Bedrock client
bedrock_client = boto3.client("bedrock-runtime", region_name="us-west-2")

# 2. Create an LLM object (Claude model via Bedrock)
llm = ChatBedrockConverse(
    model="anthropic.claude-3-5-sonnet-20240620-v1:0",  # update if you have another Claude model
    temperature=0,
    max_tokens=256,
    client=bedrock_client,
)

# os.environ["LANGSMITH_TRACING"] = "true"
# os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
# os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
# os.environ["LANGSMITH_PROJECT"] = "langchain-academy"

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

model = AzureChatOpenAI(
    model="gpt-4o",
    api_version="2024-08-01-preview",
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
)

instructions = (
    "You are a Marketing Research Assistant. "
    "Your task is to analyze market trends, competitor strategies, "
    "and customer insights. "
    "Provide concise, data-backed summaries and actionable recommendations. "
)
system_message = [SystemMessage(content=instructions)]


def chat(state: State) -> dict:
    messages = system_message + state["messages"]
    message = model.invoke(messages)  # Generate response
    return {"messages": [message]}  # Return updated messages
