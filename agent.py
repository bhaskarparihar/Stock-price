import os
import sys
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage

# Import the custom tools
from tools import get_stock_price, search_stock_ticker

def main():
    # Load environment variables from .env
    load_dotenv()
    
    # Verify API key is available
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("Error: GROQ_API_KEY environment variable is not set.")
        print("Please create a '.env' file in the root directory containing:")
        print("GROQ_API_KEY=your_actual_groq_api_key")
        print("\nAlternatively, set it in your shell environment.")
        sys.exit(1)
        
    # Get model name from environment or use the latest default (Llama 3.3)
    model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    print(f"Initializing LangGraph Groq Agent using model '{model_name}'...")
    
    try:
        # Initialize ChatGroq LLM
        llm = ChatGroq(
            model=model_name,
            temperature=0.0,
            groq_api_key=groq_api_key
        )
        
        # Define the tools list
        tools = [search_stock_ticker, get_stock_price]
        
        # Define the system message instructions
        system_message = SystemMessage(
            content=(
                "You are an expert financial assistant specialized in tracking company stock prices.\n"
                "Your objective is to provide the current share price of a requested company.\n\n"
                "Follow these steps to answer questions:\n"
                "1. If you are not absolutely sure about the stock ticker of a company, use the 'search_stock_ticker' tool first.\n"
                "2. Once you have the stock ticker symbol, use the 'get_stock_price' tool to fetch the price.\n"
                "3. Respond back with the ticker symbol, company name, exchange, and the current stock price in a clear, user-friendly format."
            )
        )
        
        # Create the ReAct agent using langgraph (the modern replacement for AgentExecutor)
        agent_executor = create_react_agent(
            llm, 
            tools, 
            prompt=system_message
        )
        
        print("\nAgent initialized successfully! Type your query below.")
        print("Example: 'What is the share price of Apple?' or 'Check stock price of Tesla'")
        print("Type 'exit' or 'quit' to close the agent.\n")
        
        # Conversation state (list of messages)
        messages = []
        
        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ['exit', 'quit']:
                    print("Goodbye!")
                    break
                
                print("\nAgent is thinking...")
                messages.append(("user", user_input))
                
                # Invoke the graph agent
                response = agent_executor.invoke({
                    "messages": messages
                })
                
                # Update the message history with the outputs
                messages = response["messages"]
                
                # The last message is the agent's response
                print(f"\nAgent: {messages[-1].content}\n")
                
                # Limit history length to prevent context window explosion
                if len(messages) > 20:
                    messages = messages[-20:]
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}\n")
                
    except Exception as e:
        print(f"Failed to initialize the agent: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
