import re
import os
import requests
import json

def perform_gap_analysis(resume_text, jd_text):
    """
    Performs a detailed, AI-powered gap analysis between a resume and a job description.
    This new version provides a much more content-rich and structured analysis, including
    actionable next steps that guide the user to other modules.
    """
    API_KEY = "AIzaSyCYaWuNB0Ff43sWRTojqOLX4mOF4EoTHTQ" # IMPORTANT: Paste your Google AI Studio API Key here
    if not API_KEY:
        return {"error": "API Key is missing from utils/gap_analyzer.py"}

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
    
    prompt = f"""
    You are an expert HR analyst and career coach. Your task is to perform a highly detailed gap analysis between a candidate's resume and a job description.
    Provide a rich, professional analysis in a valid JSON format.

    Here is the candidate's resume:
    ---
    {resume_text}
    ---

    Here is the job description:
    ---
    {jd_text}
    ---

    Analyze both documents and return a single JSON object with the following detailed structure:
    {{
      "overall_fit_score": <An integer from 0 to 100 representing the overall fit>,
      "analysis_summary": "<A 2-3 sentence summary of the candidate's fit for the role, highlighting key strengths and gaps>",
      "skill_analysis": {{
        "matched_skills": [<A list of strings of the top 5-7 most important skills found in BOTH the resume and the JD>],
        "missing_skills": [<A list of strings of the top 5-7 most critical skills found in the JD but MISSING from the resume>],
        "unique_skills": [<A list of strings of 2-3 valuable skills the candidate has that are NOT required by the JD>]
      }},
      "experience_analysis": {{
        "strengths": "<A sentence describing how the candidate's experience aligns well with the role, citing an example.>",
        "gaps": "<A sentence identifying specific experience gaps (e.g., 'Lacks experience in enterprise-level software deployment').>"
      }},
      "next_steps": [
          {{
              "title": "Bridge Your Skill Gaps",
              "suggestion": "Your resume is missing some key skills for this role. To create a personalized learning plan to acquire these skills...",
              "action": "Go to the 'Roadmap' Module"
          }},
          {{
              "title": "Tailor Your Resume",
              "suggestion": "To improve your chances, you should tailor your resume to this specific job description. For a detailed, line-by-line analysis and suggestions...",
              "action": "Go to the 'Analysis' Module"
          }},
          {{
              "title": "Prepare for the Interview",
              "suggestion": "Be ready to discuss how your unique skills can benefit the company. To practice your answers and get interview coaching...",
              "action": "Go to the 'AI  Mentor' Module"
          }}
      ]
    }}
    """

    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"response_mime_type": "application/json"}
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=60)
        response.raise_for_status()
        
        result_json_string = response.json()['candidates'][0]['content']['parts'][0]['text']
        analysis_result = json.loads(result_json_string)
        
        # Ensure 'fit_score' is present for the main UI
        analysis_result['fit_score'] = analysis_result.get('overall_fit_score', 0)
        return analysis_result

    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return {"error": f"Failed to parse AI response: {e}. Response was: {response.text}"}

