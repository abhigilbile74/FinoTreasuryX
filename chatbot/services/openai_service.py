"""
OpenAI service wrapper for a financial chatbot.
Uses the OPENAI_API_KEY environment variable (loaded from .env or system).
If no key is configured, it returns a graceful, rule-based default reply.
Uses the modern 'openai' Python library syntax (v1.x+).
"""
from dotenv import load_dotenv
from openai import OpenAI
import os
from django.conf import settings # Assumes Django settings are configured

# 1. Load variables from the .env file (if it exists)
# This should be called early in your application's loading process.
load_dotenv()

# 2. Retrieve the API Key from environment or Django settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or getattr(settings, "OPENAI_API_KEY", None)

def gpt_reply(prompt: str, user_id: str = None, model: str = "sentence-transformers/all-MiniLM-L6-v2") -> str:
    """
    Sends a prompt to the OpenAI Chat Completion API.

    Args:
        prompt (str): The user's question or message.
        user_id (str, optional): A unique ID for the user (recommended for
                                 monitoring). Defaults to None.
        model (str, optional): The OpenAI model to use. Defaults to "gpt-4o-mini".

    Returns:
        str: The AI's response or an error/fallback message.
    """
    if not OPENAI_API_KEY:
        # Fallback: no OpenAI key — return safe, rule-based acknowledgement
        return (
            "I can help with general financial questions, budgeting, and savings advice. "
            "For example, try 'How to save $20000 per year?' or 'Explain compound interest'. "
            "To enable advanced natural language answers, set the OPENAI_API_KEY environment variable."
        )

    try:
        # Instantiate the client with the API key
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Build the API call parameters
        params = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    # Specific, safety-focused prompt for a financial assistant
                    "content": "You are a concise, helpful, and objective personal finance assistant. You provide general advice on budgeting, saving, and investing. You must explicitly avoid giving legal, tax, or specific investment advice, and must not ask for or store sensitive user data."
                },
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 400,
            "temperature": 0.2,
        }
        
        # Conditionally add user ID (recommended practice)
        if user_id:
            params["user"] = user_id
            
        # Call the modern Chat Completions API
        response = client.chat.completions.create(**params)
        
        # Extract content from the new response object structure
        text = response.choices[0].message.content.strip()
        return text
        
    except Exception as exc:
        # Graceful error handling for API connection issues or other exceptions
        print(f"OpenAI API Error: {exc}") # Log the error for debugging
        return f"Sorry, I couldn't connect to the AI service. Please check the API key and network connection: {str(exc)}"

# --- Example Usage (How to test this function) ---
if __name__ == '__main__':
    # NOTE: You must have an OPENAI_API_KEY set in your .env file or environment
    #       for this test to return an AI response.

    print("--- Test 1: General Advice ---")
    advice_prompt = "What is a good strategy for saving for a down payment on a house?"
    reply = gpt_reply(advice_prompt, user_id="test_user_123")
    print(f"User: {advice_prompt}")
    print(f"Bot: {reply}\n")

    print("--- Test 2: Tax/Legal Query (Should be avoided) ---")
    tax_prompt = "What tax deductions can I claim for my business expenses this year?"
    reply = gpt_reply(tax_prompt)
    print(f"User: {tax_prompt}")
    print(f"Bot: {reply}")


