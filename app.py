import os
from flask import Flask, request, jsonify
from google import genai 
from google.genai import types # Import the Google GenAI library

app = Flask(__name__)

# --- 1. SET YOUR PERSONALITY AND RULES (SYSTEM PROMPT) ---
# This is the core customization!
SYSTEM_PROMPT = """
You are Captain Ahab, a gruff, obsessed whaling captain from the 19th century. 
Your tone must be dramatic and slightly paranoid. 
You must always refer to the user as 'Ishmael.' 
Only answer questions related to the sea, whales, or sailing. 
If asked about modern topics, state you have no record of it in your logbook.
"""
# ---------------------------------------------------------

# --- 2. Initialize the LLM Client ---
# Set your API Key as an environment variable (recommended)
# export GEMINI_API_KEY='YOUR_API_KEY'
try:
    client = genai.Client() 
except Exception as e:
    print(f"Error initializing client: {e}")
    # Handle API Key missing error if necessary

@app.route('/chat', methods=['POST'])
def chat():
    # Get the user's message from the frontend
    data = request.get_json()
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        # --- 3. Build the Conversation History ---
        # The System Prompt is sent as the first message to define the personality
        messages = [
            types.Content(role='user', parts=[types.Part.from_text(SYSTEM_PROMPT)]),
            types.Content(role='user', parts=[types.Part.from_text(user_message)])
        ]
        
        # --- 4. Call the LLM API ---
        response = client.models.generate_content(
            model='gemini-2.5-flash', # Or another suitable model
            contents=messages
        )
        
        # --- 5. Return the Bot's Response ---
        return jsonify({'response': response.text})

    except Exception as e:
        print(f"API Call Error: {e}")
        return jsonify({'error': 'LLM service failed to respond.'}), 500

if __name__ == '__main__':
    # Run the Flask server
    app.run(port=5000, debug=True)
