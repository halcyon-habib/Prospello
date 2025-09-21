import requests
import json
import time

# You can use the same API key from your AI Mentor
API_KEY = "AIzaSyCYaWuNB0Ff43sWRTojqOLX4mOF4EoTHTQ" 

def generate_career_roadmap(resume_text, goal_text, roadmap_type):
    """
    Generates a personalized career roadmap using the Gemini API.
    It can generate a roadmap based on a general job role or a specific job description.
    """
    if roadmap_type == "Job Role":
        prompt = f"""
        Act as an expert career coach and strategist.
        Based on the user's resume provided below, create a comprehensive, week-by-week, 30-day career roadmap to help them become a strong candidate for a '{goal_text}' role.

        The roadmap should be structured into four weeks. For each week, provide actionable tasks covering:
        1.  **Technical Skills to Learn:** Specific languages, frameworks, or tools.
        2.  **Projects to Build:** A concrete project idea to add to their portfolio.
        3.  **Key Concepts to Master:** Important theoretical knowledge.
        4.  **Networking & Professional Growth:** Tips on how to connect with people or improve their brand.

        Format the output clearly with headings for each week.

        ---
        USER'S RESUME:
        {resume_text}
        ---
        """
    else: # roadmap_type == "Job Description"
        prompt = f"""
        Act as an expert career coach and talent acquisition specialist.
        You are given a user's resume and a specific job description they are targeting. Your task is to perform a gap analysis and create a highly specific, week-by-week, 30-day action plan to prepare the user for this exact role.

        The roadmap should be structured into four weeks. For each week, provide actionable tasks that directly address the requirements in the job description that are missing from the user's resume. Cover these areas:
        1.  **Priority Skills to Learn:** Focus on the most critical missing skills from the JD.
        2.  **Targeted Project Idea:** A project that would directly demonstrate the missing skills.
        3.  **Interview Preparation:** What to focus on based on the JD.
        4.  **Resume Keywords to Add:** Specific keywords from the JD to incorporate.

        Format the output clearly with headings for each week.

        ---
        USER'S RESUME:
        {resume_text}
        ---
        TARGET JOB DESCRIPTION:
        {goal_text}
        ---
        """

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.6,
            "topK": 1,
            "topP": 1,
            "maxOutputTokens": 8192, # FIX: Increased token limit for longer responses
        }
    }
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()
        
        if 'candidates' in result and result['candidates']:
            return result['candidates'][0]['content']['parts'][0]['text']
        return "Could not generate a roadmap. The model returned an empty response."
    except requests.exceptions.RequestException as e:
        return f"API request failed: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

