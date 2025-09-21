import requests
import json

# It's recommended to have the API_KEY in an environment variable for security
# For this project, we will place it here for simplicity.
API_KEY = "AIzaSyCYaWuNB0Ff43sWRTojqOLX4mOF4EoTHTQ" # IMPORTANT: Paste your Google AI Studio API Key here

def parse_resume_with_ai(resume_text):
    """
    Uses a RAG-based approach with the Gemini API to parse the entire resume
    into a structured JSON object. This is a much more powerful and accurate
    method than traditional regex parsing.
    """
    if not API_KEY:
        return {"error": "API Key is missing. Please add it to utils/parser.py"}

    # FIX: Updated the model name to the latest version to resolve the 404 error
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
    
    # This JSON schema tells the AI exactly how to structure its response.
    json_schema = {
        "type": "OBJECT",
        "properties": {
            "profile": {
                "type": "OBJECT",
                "properties": {
                    "name": {"type": "STRING"},
                    "email": {"type": "STRING"},
                    "phone": {"type": "STRING"},
                    "linkedin": {"type": "STRING"},
                    "github": {"type": "STRING"}
                }
            },
            "summary": {"type": "STRING"},
            "education": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "degree": {"type": "STRING"},
                        "institution": {"type": "STRING"},
                        "dates": {"type": "STRING"},
                        "details": {"type": "STRING"}
                    }
                }
            },
            "skills": {
                "type": "OBJECT",
                "properties": {
                    "programming": {"type": "ARRAY", "items": {"type": "STRING"}},
                    "tools_platforms": {"type": "ARRAY", "items": {"type": "STRING"}},
                    "libraries_frameworks": {"type": "ARRAY", "items": {"type": "STRING"}},
                    "soft_skills": {"type": "ARRAY", "items": {"type": "STRING"}}
                }
            },
            "experience": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "role": {"type": "STRING"},
                        "company": {"type": "STRING"},
                        "dates": {"type": "STRING"},
                        "responsibilities": {"type": "ARRAY", "items": {"type": "STRING"}}
                    }
                }
            },
            "projects": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "name": {"type": "STRING"},
                        "description": {"type": "STRING"},
                        "link": {"type": "STRING"}
                    }
                }
            }
        }
    }

    # The prompt instructs the AI on its role and the task.
    prompt = f"""
    You are an expert resume parsing AI. Your task is to meticulously read the following resume text and extract every detail into the specified JSON format. Do not miss any information. Pay close attention to dates, job responsibilities, project descriptions, and skill categorization.

    Resume Text:
    ---
    {resume_text}
    ---
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": json_schema,
            "temperature": 0.2,
        }
    }

    try:
        response = requests.post(api_url, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status() # Raise an exception for bad status codes
        
        # Extract the JSON string from the response
        response_json = response.json()
        json_string = response_json['candidates'][0]['content']['parts'][0]['text']
        
        # Parse the JSON string into a Python dictionary
        parsed_data = json.loads(json_string)
        return parsed_data

    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return {"error": f"Failed to parse AI response: {e}. The response might be malformed."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

