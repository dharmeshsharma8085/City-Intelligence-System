from dotenv import load_dotenv
load_dotenv()

import os
import requests

from rich import print
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient
from langchain_mistralai import ChatMistralAI


# Weather tool
@tool
def get_weather(city: str) -> str:
    """Get the current weather of a city."""

    API_KEY = os.getenv("OPENWEATHER_API_KEY")

    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city},IN&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    print("DEBUG:", data)

    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Could not fetch weather')}"

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return f"Weather in {city}: {desc}, {temp}°C"


# Test weather tool
result = get_weather.invoke("Pilani")
print(result)


# Tavily client
tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


# News tool
@tool
def get_news(city: str) -> str:
    """Get latest news about a city."""

    response = tavily_client.search(
        query=f"latest news in {city}",
        search_depth="basic",
        max_results=3
    )

    results = response.get("results", [])

    if not results:
        return f"No news found for {city}"

    news_list = []

    for r in results:
        title = r.get("title", "No title")
        url = r.get("url", "")
        snippet = r.get("content", "")

        news_list.append(
            f"- {title}\n"
            f"{url}\n"
            f"{snippet[:100]}..."
        )

    return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)


# Test news tool
print(get_news.invoke("Pilani"))


# Create LLM
llm = ChatMistralAI(
    model="mistral-small-2506"
)


# Tool registry
tools = {
    "get_weather": get_weather,
    "get_news": get_news
}


# Bind tools to LLM
llm_with_tools = llm.bind_tools(
    [get_weather, get_news]
)


# Agent loop
messages = []

print("\nCity Intelligence System")
print("Type 0 to exit\n")

while True:

    user_input = input("You: ")

    if user_input == "0":
        print("Goodbye!")
        break

    # Add user message
    messages.append(
        HumanMessage(content=user_input)
    )

    # Agent reasoning loop
    while True:

        result = llm_with_tools.invoke(messages)
        messages.append(result)

        # Check if LLM wants to call a tool
        if result.tool_calls:

            for tool_call in result.tool_calls:

                tool_name = tool_call["name"]

                # Human approval
                confirm = input(
                    f"Agent wants to call '{tool_name}'. "
                    f"Approve? (Yes/No): "
                )

                if confirm.lower() != "yes":

                    print("Tool call denied.")

                    messages.append(
                        ToolMessage(
                            content="Tool call denied by the user.",
                            tool_call_id=tool_call["id"]
                        )
                    )

                    continue

                # Execute tool
                tool_result = tools[tool_name].invoke(
                    tool_call
                )

                # Send tool result back to LLM
                messages.append(
                    ToolMessage(
                        content=tool_result,
                        tool_call_id=tool_call["id"]
                    )
                )

            # Let LLM process tool results
            continue

        # Final answer
        else:
            print(f"Agent: {result.content}")
            break