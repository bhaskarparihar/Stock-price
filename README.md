# Stock Price Agent

A smart financial assistant built using **LangChain** and **Groq LLM API** that searches for company stock tickers and retrieves real-time stock prices using `yfinance` (Yahoo Finance).

## Features
- **Stock Ticker Auto-Lookup**: Resolves company names to their correct stock tickers (e.g., "Apple" -> "AAPL") via Yahoo Finance search api.
- **Real-Time Prices**: Fetches the latest stock price and currency using `yfinance`.
- **Conversational Interface**: Interactive command-line interface with chat history support.
- **Fast Execution**: Powered by Groq's high-speed Llama-3 model.

---

## Prerequisites
- Python 3.8 or higher.
- A **Groq API Key** (you can get one for free from the [Groq Console](https://console.groq.com/)).

---

## Setup Instructions

### 1. Clone the repository / Navigate to the folder
If you cloned the repo from GitHub:
```bash
git clone https://github.com/bhaskarparihar/Stock-price.git
cd Stock-price
```
If you are running it locally on the F drive:
```bash
cd "F:\Stock-price"
```

### 2. Create and activate a Virtual Environment
It is highly recommended to run this in a virtual environment to manage dependencies:

**On Windows (Command Prompt or PowerShell):**
```powershell
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the `.env.example` file to `.env`:
```bash
copy .env.example .env     # Windows
cp .env.example .env       # macOS/Linux
```
Open the `.env` file and replace `your_groq_api_key_here` with your actual Groq API key:
```env
GROQ_API_KEY=gsk_your_api_key_value
```

---

## How to Run

Run the agent via the terminal:
```bash
python agent.py
```

### Example Usage:
```
Initializing LangChain Groq Agent using model 'llama3-70b-8192'...
Agent initialized successfully! Type your query below.

You: What is the share price of Google?
Agent is thinking...
> Entering new AgentExecutor chain...
...
> Finished chain.

Agent: The current stock price for GOOGL (Alphabet Inc.) is 176.45 USD.
```

---

## How to Publish to GitHub
To push this code to your GitHub repository `https://github.com/bhaskarparihar/Stock-price.git`, run the following commands in your project directory:

```bash
git init
git add .
git commit -m "Initial commit: LangChain Groq Stock Price Agent"
git branch -M main
git remote add origin https://github.com/bhaskarparihar/Stock-price.git
git push -u origin main
```
