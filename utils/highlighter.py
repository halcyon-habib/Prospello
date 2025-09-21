import re

# Keyword lists for highlighting
TECHNICAL_SKILLS = [
    'python', 'java', 'c++', 'c#', 'javascript', 'typescript', 'sql', 'nosql', 'mongodb', 'postgresql',
    'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring', 'aws', 'azure', 'gcp',
    'docker', 'kubernetes', 'terraform', 'git', 'jenkins', 'jira', 'tableau', 'power bi',
    'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy'
]
SOFT_SKILLS = [
    'leadership', 'teamwork', 'communication', 'problem-solving', 'critical thinking', 'creativity',
    'adaptability', 'time management', 'collaboration', 'work ethic', 'interpersonal skills'
]
ACTION_VERBS = [
    'managed', 'led', 'developed', 'engineered', 'launched', 'created', 'increased', 'reduced',
    'saved', 'implemented', 'spearheaded', 'orchestrated', 'achieved', 'improved'
]
WEAK_PHRASES = [
    'responsible for', 'assisted with', 'worked on', 'team player', 'duties included', 'highly motivated'
]

def highlight_text(text):
    """
    Analyzes text and wraps keywords in HTML spans for highlighting.
    """
    # Use word boundaries (\b) to match whole words only, ensuring safety with re.escape
    for skill in TECHNICAL_SKILLS:
        text = re.sub(r'\b(' + re.escape(skill) + r')\b', r'<span class="highlight tech">\1</span>', text, flags=re.IGNORECASE)
    for skill in SOFT_SKILLS:
        text = re.sub(r'\b(' + re.escape(skill) + r')\b', r'<span class="highlight soft">\1</span>', text, flags=re.IGNORECASE)
    for verb in ACTION_VERBS:
        text = re.sub(r'\b(' + re.escape(verb) + r')\b', r'<span class="highlight action">\1</span>', text, flags=re.IGNORECASE)
    
    # Weak phrases may contain spaces, so don't use word boundaries at the edges
    for phrase in WEAK_PHRASES:
        text = re.sub(r'(' + re.escape(phrase) + r')', r'<span class="highlight weak">\1</span>', text, flags=re.IGNORECASE)
    
    # Preserve line breaks for the HTML display
    text_with_breaks = text.replace('\n', '<br>')
    
    # Return the HTML wrapped in a styled container
    return f"<div class='highlight-container'>{text_with_breaks}</div>"
