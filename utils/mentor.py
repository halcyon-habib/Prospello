import requests
import json
import time

# NOTE: In a real-world application, this API key would be managed securely,
# for example, using Streamlit's secrets management.
# For our project, we will leave it as a placeholder.
API_KEY = "AIzaSyCYaWuNB0Ff43sWRTojqOLX4mOF4EoTHTQ" 

def get_ai_mentor_response(user_prompt, chat_history, resume_text):
    """
    Gets a response from the Gemini API, providing the user's resume as context.
    """
    # System instruction to define the AI's persona and provide resume context.
    system_instruction = f"""
    You are "CareerCoPilot," a friendly, encouraging, and expert AI career mentor. 
    Your primary goal is to provide supportive, insightful, and actionable career advice.

    You MUST use the user's resume, provided below, to personalize your responses. 
    Reference their skills, experiences, or projects to make your advice highly relevant.

    ---
    USER'S RESUME:
    {resume_text}
    ---

    Keep your answers concise, well-structured (using bullet points for lists), and maintain a positive and professional tone.
    """

    # We will use the powerful gemini-2.5-flash-preview-05-20 model
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"

    # Construct the conversation history for the API
    contents = []
    for message in chat_history:
        # Map our 'user'/'assistant' roles to 'user'/'model' for the API
        role = "user" if message["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": message["content"]}]})
    
    # Add the current user prompt
    contents.append({"role": "user", "parts": [{"text": user_prompt}]})

    payload = {
        "contents": contents,
        "systemInstruction": {
            "parts": [{"text": system_instruction}]
        },
        "generationConfig": {
            "temperature": 0.7,
            "topK": 1,
            "topP": 1,
            "maxOutputTokens": 8192, # FIX: Increased token limit for longer responses
        }
    }

    headers = {'Content-Type': 'application/json'}
    
    # --- API Call with Exponential Backoff for Reliability ---
    max_retries = 5
    delay = 1  # start with 1 second
    for attempt in range(max_retries):
        try:
            response = requests.post(api_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status() # Raise an exception for bad status codes
            
            result = response.json()
            
            # Safely access the response content
            if 'candidates' in result and result['candidates']:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content'] and candidate['content']['parts']:
                    return candidate['content']['parts'][0]['text']
            
            # Handle cases where the response is valid but empty (e.g., safety filters)
            return "I'm sorry, I couldn't generate a response for that. Could you please try rephrasing your question?"

        except requests.exceptions.RequestException as e:
            print(f"API request failed on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2 # Double the delay for the next retry
            else:
                return "I'm sorry, I'm having trouble connecting to my knowledge base right now. Please try again in a moment."
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return "An unexpected error occurred. Please try again."

    return "I seem to be having some trouble. Please try again later."

 