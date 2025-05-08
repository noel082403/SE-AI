import google.generativeai as genai
import os

# Set up the Gemini API key
os.environ['GOOGLE_API_KEY'] = 'AIzaSyBr7G_IRheqrZi0oWzuB6ZLOJb875ryfts'

# Configure the model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt: str) -> str:
    """
    Sends a prompt to Google Gemini API and returns the response.
    
    Args:
        prompt (str): The input prompt for the Gemini model.

    Returns:
        str: The model's response.
    """
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")  # Use the correct model
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else "No response received."
    except Exception as e:
        return f"Error: {e}"
