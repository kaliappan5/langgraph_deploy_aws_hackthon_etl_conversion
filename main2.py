import asyncio

from langchain_core.messages import HumanMessage
from langgraph_sdk import get_client

LANGGRAPH_SERVER_URL = "http://localhost:8123"


async def main() -> None:
    # Initialize the LangGraph client
    client = get_client(url=LANGGRAPH_SERVER_URL)

    # Fetch the list of available assistants from the server
    assistants = await client.assistants.search()

    # Select the first assistant from the list
    agent = assistants[0]

    # Create a new conversation thread with the assistant
    thread = await client.threads.create()

    # Prepare the user message
    #user_message = {"messages": [HumanMessage(content="Hi")]}
    #user_message = {"messages": [HumanMessage(content="What is the weather like today?")]}


    # Prepare and send multiple user messages
    messages = [
        "Hi",
        "What are the top 3 marketing strategies for 2025?",
        "Can you summarize the latest AI trends?"
    ]
    for msg in messages:
        user_message = {"messages": [HumanMessage(content=msg)]}
        async for chunk in client.runs.stream(
            thread_id=thread["thread_id"],
            assistant_id=agent["assistant_id"],
            input=user_message,
            stream_mode="values",
        ):
            if chunk.data and chunk.event != "metadata":
                print(chunk.data["messages"][-1]["content"])

if __name__ == "__main__":
    asyncio.run(main())
