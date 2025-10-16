import boto3
from langchain_aws import ChatBedrockConverse
from langgraph.graph import StateGraph, END

# 1. Initialize Bedrock client
bedrock_client = boto3.client("bedrock-runtime", region_name="us-west-2")

# 2. Create an LLM object (Claude model via Bedrock)
llm = ChatBedrockConverse(
    model="anthropic.claude-3-5-sonnet-20240620-v1:0",  # update if you have another Claude model
    temperature=0,
    max_tokens=256,
    client=bedrock_client,
)

# 3. Define a simple agent node (function)
def echo_agent(state):
    user_input = state["user_input"]
    # The agent uses the Claude model to answer
    answer = llm.invoke(f"Echo this back to the user: {user_input}")
    return {"user_input": user_input, "output": answer}

# 4. Define the graph state
class EchoState(dict):
    pass

# 5. Build the graph (one node, simple flow)
graph = StateGraph(EchoState)
graph.add_node("echo", echo_agent)
graph.set_entry_point("echo")
graph.add_edge("echo", END)
compiled_graph = graph.compile()

# 6. Run the graph
if __name__ == "__main__":
    user_input = input("Type something to echo: ")
    result = compiled_graph.invoke({"user_input": user_input})
    print("Model output:", result["output"])