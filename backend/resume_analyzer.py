import os
from typing import Dict, List
from backend.llm import generate_with_ai

# Common action verbs for resumes
ACTION_VERBS = [
    "achieved", "improved", "trained", "managed", "created", "designed",
    "developed", "implemented", "increased", "decreased", "led", "launched",
    "optimized", "reduced", "streamlined", "transformed", "built", "delivered"
]

# Industry-specific keywords
INDUSTRY_KEYWORDS = {
    "technology" : [
        "agile", "scrum", "cloud", "api", "microservices", "devops", "ci/cd",
        "python", "java", "react", "kubernetes", "aws", "azure", "docker"
    ],
    "finance" : [
        "analysis", "forecasting", "budgeting", "financial modeling", "compliance",
        "risk management", "excel", "sql", "bloomberg", "gaap", "sox"
    ],
    "marketing" : [
        "seo", "sem", "analytics", "campaigns", "conversion", "roi", "engagement",
        "social media", "content strategy", "brand", "google analytics"
    ],
    "healthcare" : [
        "patient care", "hipaa", "ehr", "emr", "clinical", "medical records",
        "treatment", "diagnosis", "healthcare compliance", "patient safety"
    ],
    "education" : [
        "curriculum", "lesson planning", "student engagement", "assessment",
        "classroom management", "differentiation", "educational technology"
    ],
    "general" : [
        "communication", "teamwork", "leadership", "problem-solving", "organization",
        "time management", "customer service", "microsoft office"
    ]
}


def calculate_resume_score ( resume_text: str, industry: str ) -> int :
    """Calculate a basic resume score based on various factors."""
    score = 0
    text_lower = resume_text.lower()

    # Check for action verbs (20 points)
    action_verb_count = sum( 1 for verb in ACTION_VERBS if verb in text_lower )
    score += min( 20, action_verb_count * 2 )

    # Check for quantifiable achievements (20 points)
    has_numbers = any( char.isdigit() for char in resume_text )
    if has_numbers :
        score += 20

    # Check for industry keywords (30 points)
    keywords = INDUSTRY_KEYWORDS.get( industry, INDUSTRY_KEYWORDS["general"] )
    keyword_count = sum( 1 for keyword in keywords if keyword in text_lower )
    score += min( 30, keyword_count * 3 )

    # Check length (10 points)
    word_count = len( resume_text.split() )
    if 200 <= word_count <= 800 :
        score += 10
    elif word_count > 100 :
        score += 5

    # Check formatting indicators (20 points)
    if any( indicator in resume_text for indicator in ['\n- ', '• ', '* '] ) :
        score += 10
    if resume_text.count( '\n\n' ) >= 2 :  # Has sections
        score += 10

    return min( 100, score )


def analyze_resume ( resume_text: str, industry: str, target_role: str ) -> Dict :
    """
    Analyze a resume and provide detailed feedback.
    """
    score = calculate_resume_score( resume_text, industry )

    # Generate AI analysis if available
    analysis_prompt = f"""Analyze this resume for a {target_role} position in the {industry} industry.

Resume:
{resume_text}

Provide a brief, constructive analysis covering:
1. Overall impression
2. Key strengths
3. Areas for improvement

Keep it concise and actionable."""

    analysis = generate_with_ai( analysis_prompt )

    # Identify strengths and weaknesses
    strengths = []
    weaknesses = []

    text_lower = resume_text.lower()

    # Check strengths
    if any( verb in text_lower for verb in ACTION_VERBS[:5] ) :
        strengths.append( "Uses strong action verbs" )
    if any( char.isdigit() for char in resume_text ) :
        strengths.append( "Includes quantifiable achievements" )
    keywords = INDUSTRY_KEYWORDS.get( industry, INDUSTRY_KEYWORDS["general"] )
    if sum( 1 for kw in keywords if kw in text_lower ) >= 3 :
        strengths.append( "Contains relevant industry keywords" )

    # Check weaknesses
    if not any( verb in text_lower for verb in ACTION_VERBS ) :
        weaknesses.append( "Lacks strong action verbs" )
    if not any( char.isdigit() for char in resume_text ) :
        weaknesses.append( "Missing quantifiable achievements" )
    if len( resume_text.split() ) < 100 :
        weaknesses.append( "Content is too brief" )
    if resume_text.count( '\n' ) < 5 :
        weaknesses.append( "Needs better formatting/structure" )

    return {
        "score" : score,
        "analysis" : analysis,
        "strengths" : strengths or ["Resume has potential"],
        "weaknesses" : weaknesses or ["Looking good overall"]
    }


def improve_resume ( resume_text: str, industry: str, target_role: str ) -> Dict :
    """
    Generate specific improvement suggestions.
    """
    prompt = f"""You are an expert resume writer. Improve this resume content for a {target_role} position in {industry}.

Original content:
{resume_text}

Provide 5 specific, actionable improvements. For each improvement:
1. Use strong action verbs
2. Add quantifiable metrics where possible
3. Make it more impactful and concise
4. Tailor it to the {target_role} role

Format each improvement as a complete bullet point."""

    ai_response = generate_with_ai( prompt )

    # Parse improvements from AI response
    improvements = []
    if ai_response :
        lines = ai_response.strip().split( '\n' )
        for line in lines :
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith( '-' ) or line.startswith( '•' )) :
                # Remove numbering/bullets
                clean_line = line.lstrip( '0123456789.-•) ' ).strip()
                if clean_line :
                    improvements.append( clean_line )

    # Ensure we have at least some improvements
    if not improvements :
        improvements = [
            "Start with strong action verbs like 'Led', 'Developed', 'Achieved'",
            "Add quantifiable metrics (e.g., 'Increased sales by 25%')",
            "Use industry-specific keywords relevant to " + industry,
            "Keep bullet points concise and impactful",
            "Focus on achievements rather than responsibilities"
        ]

    return {
        "improvements" : improvements[:5],
        "original_text" : resume_text
    }


def optimize_for_ats ( resume_text: str, industry: str, target_role: str ) -> Dict :
    """
    Optimize resume for Applicant Tracking Systems.
    """
    keywords = INDUSTRY_KEYWORDS.get( industry, INDUSTRY_KEYWORDS["general"] )
    text_lower = resume_text.lower()

    # Find missing keywords
    missing_keywords = [kw for kw in keywords if kw not in text_lower]
    keywords_to_add = missing_keywords[:10]

    prompt = f"""Optimize this resume for Applicant Tracking Systems (ATS) for a {target_role} position.

Original resume:
{resume_text}

Requirements:
1. Add these relevant keywords naturally: {', '.join( keywords_to_add[:5] )}
2. Use standard section headers (e.g., "EXPERIENCE", "SKILLS", "EDUCATION")
3. Remove special characters and complex formatting
4. Keep it ATS-friendly while maintaining readability

Provide the optimized version."""

    optimized_text = generate_with_ai( prompt )

    # Calculate ATS score
    ats_score = 50  # Base score

    # Keywords present
    keyword_count = sum( 1 for kw in keywords if kw in text_lower )
    ats_score += min( 30, keyword_count * 3 )

    # Standard sections
    standard_sections = ["experience", "education", "skills"]
    section_count = sum( 1 for section in standard_sections if section in text_lower )
    ats_score += section_count * 7

    return {
        "optimized_text" : optimized_text or resume_text,
        "keywords_added" : keywords_to_add[:5],
        "ats_score" : min( 100, ats_score )
    }