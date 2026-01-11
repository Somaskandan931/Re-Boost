"""
Resume Information Extractor
Extracts structured data from PDF, DOCX, and TXT resume files.
"""

import re
from typing import Dict, List
from backend.llm import generate_with_ai

def extract_email(text: str) -> str:
    """Extract email address from text."""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    return match.group(0) if match else ""

def extract_phone(text: str) -> str:
    """Extract phone number from text."""
    phone_patterns = [
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\+\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    ]

    for pattern in phone_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return ""

def extract_links(text: str) -> Dict[str, str]:
    """Extract LinkedIn, GitHub, and other links."""
    links = {}

    # LinkedIn
    linkedin_pattern = r'linkedin\.com/in/[\w-]+'
    linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
    if linkedin_match:
        links["linkedin"] = "https://" + linkedin_match.group(0)

    # GitHub
    github_pattern = r'github\.com/[\w-]+'
    github_match = re.search(github_pattern, text, re.IGNORECASE)
    if github_match:
        links["github"] = "https://" + github_match.group(0)

    # Website
    website_pattern = r'https?://(?:www\.)?[\w.-]+\.[\w]{2,}'
    for match in re.finditer(website_pattern, text):
        url = match.group(0)
        if 'linkedin' not in url.lower() and 'github' not in url.lower():
            links["website"] = url
            break

    return links

def extract_from_text_with_ai(text: str) -> Dict:
    """Use AI to extract structured information from resume text."""

    prompt = f"""Extract structured information from this resume text and return it as JSON.

Resume Text:
{text[:3000]}  # Limit to first 3000 chars

Extract the following information:
1. Personal Information: name, email, phone, location
2. Education: degree, institution, field, graduation date, GPA
3. Work Experience: job title, company, dates, location, key achievements
4. Projects: project name, description, technologies, links
5. Skills: technical skills list
6. Certifications: certification name, issuer, date

Return as valid JSON with this structure:
{{
  "personal_info": {{"name": "", "email": "", "phone": "", "location": ""}},
  "education": [{{"degree": "", "institution": "", "field": "", "graduation": "", "gpa": ""}}],
  "experience": [{{"title": "", "company": "", "start_date": "", "end_date": "", "description": ""}}],
  "projects": [{{"name": "", "description": "", "technologies": "", "github": ""}}],
  "skills": [],
  "certifications": [{{"name": "", "issuer": "", "date": ""}}]
}}

Only return the JSON, no explanation."""

    try:
        ai_response = generate_with_ai(prompt, max_tokens=1500)

        # Try to parse JSON from response
        import json

        # Clean response (remove markdown code blocks if present)
        clean_response = ai_response.strip()
        if clean_response.startswith('```'):
            clean_response = clean_response.split('```')[1]
            if clean_response.startswith('json'):
                clean_response = clean_response[4:]
        clean_response = clean_response.strip()

        data = json.loads(clean_response)
        return data

    except Exception as e:
        print(f"AI extraction failed: {e}")
        return None

def extract_basic_info(text: str) -> Dict:
    """Extract basic information using regex patterns."""

    lines = text.split('\n')

    # Try to get name from first non-empty line
    name = ""
    for line in lines[:5]:
        line = line.strip()
        if line and len(line.split()) <= 4 and not '@' in line:
            name = line
            break

    # Extract contact info
    email = extract_email(text)
    phone = extract_phone(text)
    links = extract_links(text)

    # Extract sections
    education = []
    experience = []
    projects = []
    skills = []
    certifications = []

    # Simple section detection
    edu_section = re.search(r'education\s*\n(.*?)(?=\n(?:experience|projects|skills|certification)|\Z)',
                           text, re.IGNORECASE | re.DOTALL)
    if edu_section:
        edu_text = edu_section.group(1)
        # Try to parse education entries
        degree_patterns = [r'(Bachelor|Master|PhD|B\.S\.|M\.S\.|Ph\.D\.)[^\n]+']
        for pattern in degree_patterns:
            matches = re.finditer(pattern, edu_text, re.IGNORECASE)
            for match in matches:
                education.append({
                    "degree": match.group(0).strip(),
                    "institution": "",
                    "field": "",
                    "graduation": "",
                    "gpa": ""
                })

    # Skills extraction
    skills_section = re.search(r'skills?\s*[:\n](.*?)(?=\n(?:experience|education|projects|certification)|\Z)',
                              text, re.IGNORECASE | re.DOTALL)
    if skills_section:
        skills_text = skills_section.group(1)
        # Split by common separators
        skill_items = re.split(r'[,;•\n]', skills_text)
        skills = [s.strip() for s in skill_items if s.strip() and len(s.strip()) > 2]

    return {
        "personal_info": {
            "name": name,
            "email": email,
            "phone": phone,
            "location": "",
            "linkedin": links.get("linkedin", ""),
            "github": links.get("github", ""),
            "website": links.get("website", ""),
            "summary": ""
        },
        "education": education,
        "experience": experience,
        "projects": projects,
        "skills": skills[:20],  # Limit to 20 skills
        "certifications": certifications,
        "links": links
    }

def extract_from_pdf(content: bytes) -> Dict:
    """Extract information from PDF resume."""
    try:
        from pypdf import PdfReader
        import io

        pdf_file = io.BytesIO(content)
        pdf_reader = PdfReader(pdf_file)

        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Try AI extraction first
        ai_result = extract_from_text_with_ai(text)
        if ai_result:
            return ai_result

        # Fallback to basic extraction
        return extract_basic_info(text)

    except Exception as e:
        print(f"PDF extraction error: {e}")
        return extract_basic_info("")

def extract_from_docx(content: bytes) -> Dict:
    """Extract information from DOCX resume."""
    try:
        import docx
        import io

        doc_file = io.BytesIO(content)
        doc = docx.Document(doc_file)

        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])

        # Try AI extraction first
        ai_result = extract_from_text_with_ai(text)
        if ai_result:
            return ai_result

        # Fallback to basic extraction
        return extract_basic_info(text)

    except Exception as e:
        print(f"DOCX extraction error: {e}")
        return extract_basic_info("")

def extract_from_txt(content: bytes) -> Dict:
    """Extract information from TXT resume."""
    try:
        text = content.decode('utf-8')

        # Try AI extraction first
        ai_result = extract_from_text_with_ai(text)
        if ai_result:
            return ai_result

        # Fallback to basic extraction
        return extract_basic_info(text)

    except Exception as e:
        print(f"TXT extraction error: {e}")
        return extract_basic_info("")