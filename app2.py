from dotenv import load_dotenv
load_dotenv()

import os
import requests
import streamlit as st
from datetime import datetime

from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient
from langchain_mistralai import ChatMistralAI


# Page configuration
st.set_page_config(
    page_title="City Intelligence System",
    page_icon="🤖",
    layout="wide"
)


# Custom CSS
st.markdown("""
<style>

    .stApp {
        background: #0b0f14;
        color: #f5f5f5;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1rem;
    }

    /* Header */
    .main-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        text-align: center;
        color: #9ca3af;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #11161d;
        border-right: 1px solid #252b33;
    }

    .sidebar-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #3b82f6;
        margin-bottom: 0;
    }

    .sidebar-subtitle {
        font-size: 1.1rem;
        color: #d1d5db;
    }

    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 1.5rem;
    }

    /* Feature cards */
    .feature-card {
        padding: 1rem;
        border-radius: 14px;
        margin: 0.7rem 0;
        border: 1px solid #2a3038;
    }

    .weather-card {
        background: #162235;
    }

    .news-card {
        background: #14251d;
    }

    .feature-title {
        font-weight: 700;
        font-size: 1rem;
        color: #f3f4f6;
    }

    .feature-text {
        color: #9ca3af;
        font-size: 0.9rem;
    }

    /* Developer footer */
    .footer {
        text-align: center;
        color: #6b7280;
        margin-top: 1rem;
        font-size: 0.9rem;
    }

    .developer {
        color: #3b82f6;
        font-weight: 700;
    }

</style>
""", unsafe_allow_html=True)


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

    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Could not fetch weather')}"

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return f"Weather in {city}: {desc}, {temp}°C"


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
            f"{snippet[:150]}..."
        )

    return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)


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


# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_tool" not in st.session_state:
    st.session_state.pending_tool = None


# Sidebar
with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🤖 City Intelligence</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">System</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        '<div class="section-title">ℹ️ About</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Ask anything about a city to get "
        "current weather information and latest news."
    )

    st.divider()

    st.markdown(
        '<div class="section-title">✨ Features</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="feature-card weather-card">
        <div class="feature-title">☀️ Weather</div>
        <div class="feature-text">
            Get current weather information of a city.
        </div>
    </div>

    <div class="feature-card news-card">
        <div class="feature-title">📰 News</div>
        <div class="feature-text">
            Get latest news and headlines about a city.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown(
        '<div class="section-title">❓ How to use</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    - Type your question about any city.
    - I will fetch weather or news information.
    - You will be asked before using a tool.
    """)

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_tool = None
        st.rerun()


# Main header
col1, col2 = st.columns([5, 1])

with col1:

    st.markdown(
        '<div class="main-title">City Intelligence System</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Your smart assistant for weather updates and latest news.'
        '</div>',
        unsafe_allow_html=True
    )

with col2:

    current_time = datetime.now().strftime("%I:%M %p")

    st.markdown(
        f"""
        <div style="
            text-align: right;
            color: #d1d5db;
            font-size: 1rem;
            padding-top: 1rem;
            font-weight: 600;
        ">
            🕐 {current_time}
        </div>
        """,
        unsafe_allow_html=True
    )


# Welcome message
if not st.session_state.messages:

    with st.chat_message("assistant", avatar="🤖"):

        st.markdown(
            "### Hello! 👋\n"
            "I can help you with **weather** and **latest news** "
            "of any city.\n\n"
            "Try asking:\n"
            "- What's the weather in Pilani?\n"
            "- Give me the latest news in Jaipur."
        )


# Display chat messages
for message in st.session_state.messages:

    if isinstance(message, HumanMessage):

        with st.chat_message("user", avatar="👤"):
            st.write(message.content)

    elif isinstance(message, ToolMessage):

        with st.chat_message("assistant", avatar="🤖"):
            st.write(message.content)

    else:

        if hasattr(message, "content") and message.content:

            with st.chat_message("assistant", avatar="🤖"):
                st.write(message.content)


# Human approval
if st.session_state.pending_tool:

    tool_call = st.session_state.pending_tool
    tool_name = tool_call["name"]

    st.warning(
        f"🔐 The agent wants to use **{tool_name}**. "
        "Do you approve?"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "✅ Approve",
            use_container_width=True
        ):

            # Execute approved tool
            tool_result = tools[tool_name].invoke(
                tool_call
            )

            # Add tool result to conversation
            st.session_state.messages.append(
                ToolMessage(
                    content=tool_result,
                    tool_call_id=tool_call["id"]
                )
            )

            # Remove pending tool
            st.session_state.pending_tool = None

            # Ask LLM to process tool result
            result = llm_with_tools.invoke(
                st.session_state.messages
            )

            st.session_state.messages.append(result)

            # Check if another tool is required
            if result.tool_calls:
                st.session_state.pending_tool = result.tool_calls[0]

            st.rerun()

    with col2:

        if st.button(
            "❌ Deny",
            use_container_width=True
        ):

            # Tell LLM that user denied the tool
            st.session_state.messages.append(
                ToolMessage(
                    content="Tool call denied by the user.",
                    tool_call_id=tool_call["id"]
                )
            )

            st.session_state.pending_tool = None

            # Ask LLM to respond after denial
            result = llm_with_tools.invoke(
                st.session_state.messages
            )

            st.session_state.messages.append(result)

            st.rerun()


# User input
user_input = st.chat_input(
    "Type your message here..."
)


if user_input:

    # Add user message
    st.session_state.messages.append(
        HumanMessage(content=user_input)
    )

    # Ask LLM
    result = llm_with_tools.invoke(
        st.session_state.messages
    )

    # Add LLM response
    st.session_state.messages.append(result)

    # Check if LLM wants to use a tool
    if result.tool_calls:

        st.session_state.pending_tool = result.tool_calls[0]

    st.rerun()


# Footer
st.markdown(
    '<div class="footer">'
    'Developed by <span class="developer">Dharmesh Sharma</span>'
    '</div>',
    unsafe_allow_html=True
)