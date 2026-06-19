import os
import sys
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

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
        
    # Get model name from environment or use a reliable default
    model_name = os.getenv("GROQ_MODEL", "llama3-70b-8192")
    
    print(f"Initializing LangChain Groq Agent using model '{model_name}'...")
    
    try:
        # Initialize ChatGroq LLM
        llm = ChatGroq(
            model=model_name,
            temperature=0.0,
            groq_api_key=groq_api_key
        )
        
        # Define the tools list
        tools = [search_stock_ticker, get_stock_price]
        
        # Set up system and agent prompt
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are an expert financial assistant specialized in tracking company stock prices.\n"
                "Your objective is to provide the current share price of a requested company.\n\n"
                "Follow these steps to answer questions:\n"
                "1. If you are not absolutely sure about the stock ticker of a company, use the 'search_stock_ticker' tool first.\n"
                "2. Once you have the stock ticker symbol, use the 'get_stock_price' tool to fetch the price.\n"
                "3. Respond back with the ticker symbol, company name, exchange, and the current stock price in a clear, user-friendly format."
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create the tool-calling agent
        agent = create_tool_calling_agent(llm, tools, prompt)
        
        # Create the agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True
        )
        
        print("\nAgent initialized successfully! Type your query below.")
        print("Example: 'What is the share price of Apple?' or 'Check stock price of Tesla'")
        print("Type 'exit' or 'quit' to close the agent.\n")
        
        # Empty chat history for the CLI loop
        chat_history = []
        
        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ['exit', 'quit']:
                    print("Goodbye!")
                    break
                
                print("\nAgent is thinking...")
                response = agent_executor.invoke({
                    "input": user_input,
                    "chat_history": chat_history
                })
                
                print(f"\nAgent: {response['output']}\n")
                
                # Update chat history for context (optional, simple keep-last-few-turns strategy)
                chat_history.append(("human", user_input))
                chat_history.append(("ai", response['output']))
                if len(chat_history) > 10:
                    chat_history = chat_history[-10:]
                    
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
