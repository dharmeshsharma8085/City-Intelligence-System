# City Intelligence System 🤖

An AI-powered city assistant built with **LangChain and Mistral AI** that can fetch **real-time weather** and **latest news** for cities.

The system uses tool calling and a **Human-in-the-Loop** approval mechanism, allowing the user to approve or deny tool execution before external APIs are accessed.

## ✨ Features

* 🌤️ Real-time weather information
* 📰 Latest city news
* 🤖 Mistral AI tool calling
* 🔧 Custom LangChain tools
* 🔐 Human-in-the-Loop tool approval
* 💬 Streamlit chatbot interface
* 🗑️ Clear chat functionality
* 🌙 Clean dark UI
* 🕐 Current time display

## 🛠️ Tech Stack

* **Python**
* **Streamlit**
* **LangChain**
* **Mistral AI**
* **OpenWeatherMap API**
* **Tavily API**

## 🧠 How It Works

```text
User
  ↓
Mistral AI
  ↓
Needs a tool?
  ↓
Human Approval
  ↓
Tool Execution
  ↓
Tool Result
  ↓
Mistral AI
  ↓
Final Response
```

The AI decides whether it needs weather or news information. Before executing the selected tool, the application asks the user for approval.

## 📂 Project Structure

```text
City-Intelligence-System/
│
├── app.py
├── .env
├── requirements.txt
└── README.md
```

## 🔑 Environment Variables

Create a `.env` file in the project directory:

```env
OPENWEATHER_API_KEY=your_openweather_api_key
TAVILY_API_KEY=your_tavily_api_key
MISTRAL_API_KEY=your_mistral_api_key
```

Keep your API keys private and **never upload your `.env` file to GitHub**.

Add this to `.gitignore`:

```text
.env
__pycache__/
.venv/
```

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/City-Intelligence-System.git
```

Move into the project directory:

```bash
cd City-Intelligence-System
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

## 💬 Example Queries

```text
What's the weather in Pilani?

Give me the latest news in Jaipur.

What's the weather in Delhi?

Tell me the latest news about Mumbai.
```

## 🔐 Human-in-the-Loop

Before an external tool is executed, the application asks for user approval.

```text
Agent wants to use get_weather

        ↓

   ✅ Approve
   ❌ Deny
```

This provides an additional layer of user control over tool execution.

## 🚀 Future Improvements

* Multi-city comparison
* Weather forecasts
* Better news filtering
* More city-based tools
* Conversation memory
* Streaming responses
* Improved tool approval interface
* Deployment with Streamlit Cloud

## 👨‍💻 Developer

**Dharmesh Sharma**

Built as a practical project to explore **LLM tool calling, LangChain agents, APIs, and Human-in-the-Loop AI systems**.
