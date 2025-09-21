import re
import os
import requests
import json

def analyze_resume_with_jd(resume_text, job_description):
    """
    Performs the definitive 10-point analysis using a powerful, AI-driven approach.
    This version uses an enhanced prompt for the Gemini model to ensure the most
    accurate, robust, and human-like analysis.
    """
    # Your personal API key is now included.
    API_KEY = "AIzaSyCYaWuNB0Ff43sWRTojqOLX4mOF4EoTHTQ" 
    if not API_KEY:
        return {"error": "API Key is missing from utils/resume_analyzer.py"}

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
    
    # An enhanced, highly detailed prompt for the most accurate AI analysis
    prompt = f"""
    As an expert HR analyst and career coach AI, you must perform a deep and critical 10-point analysis comparing the following resume with the job description.
    Your primary goal is accuracy. Read and understand both documents contextually. Pay close attention to extracting proper nouns like names, schools, and companies correctly.
    Your entire response must be a single, valid JSON object following the specified structure precisely.

    **Resume Text:**
    ---
    {resume_text}
    ---

    **Job Description Text:**
    ---
    {job_description}
    ---

    **JSON Output Structure:**
    {{
      "profile_summary": {{
        "name": "<Extracted Full Name>",
        "contact": "<Extracted Email & Phone>",
        "education": "<Highest Degree and Institution>",
        "experience_years": "<Total years of experience, e.g., '3+ years' or 'Entry-level'>",
        "key_skills": ["<A list of the top 5 most relevant skills found in the resume>"]
      }},
      "ats_match_score": <Integer, 0-100, based on keyword alignment and structural integrity>,
      "keyword_score": <Integer, 0-100, based on direct skill and keyword overlap>,
      "experience_relevance_score": <Integer, 0-100, based on how well the work experience aligns with the JD's requirements>,
      "formatting_score": <Integer, 0-100, based on clarity, use of bullet points, and standard sectioning>,
      "skills_match": {{
        "matched": ["<A list of skills present in both the resume and the JD>"],
        "missing": ["<A list of critical skills from the JD that are NOT in the resume>"],
        "recommended": ["<A list of 2-3 industry-standard skills for this role that are not mentioned in either document>"]
      }},
      "keyword_optimization": {{
        "missing_keywords": ["<A list of the top 5 most important keywords from the JD to add to the resume>"],
        "weak_keywords": ["<A list of any weak phrases like 'responsible for' found in the resume>"]
      }},
      "education_certifications": {{
        "missing": ["<A list of required certifications from the JD not found in the resume>"],
        "suggested": ["<A list of 2-3 relevant certifications like 'AWS Certified' that could strengthen the resume>"]
      }},
      "soft_skills_analysis": {{
        "found": ["<A list of soft skills found in the resume>"],
        "missing": ["<A list of important soft skills mentioned in the JD but not found in the resume>"]
      }},
      "formatting_ats": {{
        "structure": "<'✅ Clear and well-structured' or '⚠️ Lacks standard sections like Education or Skills'>",
        "issues": "<'None detected' or a brief description of issues like 'Long paragraphs detected, consider using bullet points'>",
        "friendliness": "<A percentage string, e.g., '90%'>"
      }},
      "improvement_suggestions": [
        "<A concrete, actionable tip for improving the resume's content>",
        "<Another actionable tip for tailoring the resume to the JD>"
      ],
      "final_report": {{
        "resume_score": <Integer, an overall score for the resume's quality and readiness>,
        "jd_match_score": <Integer, same as the ats_match_score>,
        "missing_skills_list": ["<The same list as skills_match.missing>"],
        "suggested_improvements": ["<The same list as improvement_suggestions>"]
      }}
    }}
    """

    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "response_mime_type": "application/json",
            "maxOutputTokens": 8192,
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=90)
        response.raise_for_status()
        
        result_json_string = response.json()['candidates'][0]['content']['parts'][0]['text']
        analysis_result = json.loads(result_json_string)
        
        return analysis_result

    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return {"error": f"Failed to parse the AI's response. The AI may have returned an invalid format. AI Response: {response.text if 'response' in locals() else 'No response object'}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

