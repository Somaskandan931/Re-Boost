from typing import List
from backend.llm import generate_with_ai

# Action verbs by category
ACTION_VERB_CATEGORIES = {
    "Leadership" : ["Led", "Directed", "Managed", "Supervised", "Coordinated", "Orchestrated"],
    "Achievement" : ["Achieved", "Exceeded", "Surpassed", "Delivered", "Accomplished", "Attained"],
    "Creation" : ["Developed", "Created", "Designed", "Built", "Established", "Launched"],
    "Improvement" : ["Improved", "Enhanced", "Optimized", "Streamlined", "Transformed", "Modernized"],
    "Analysis" : ["Analyzed", "Evaluated", "Assessed", "Investigated", "Researched", "Examined"],
    "Communication" : ["Presented", "Communicated", "Collaborated", "Negotiated", "Facilitated", "Influenced"]
}


def generate_suggestions ( suggestion_type: str, text: str, industry: str, target_role: str ) -> List[str] :
    """
    Generate specific suggestions based on type.

    Args:
        suggestion_type: Type of suggestion needed
        text: Original text to improve
        industry: Target industry
        target_role: Target job role

    Returns:
        List of suggestion strings
    """

    if suggestion_type == "Improve bullet points" :
        return improve_bullet_points( text, industry, target_role )

    elif suggestion_type == "Add action verbs" :
        return add_action_verbs( text, target_role )

    elif suggestion_type == "Quantify achievements" :
        return quantify_achievements( text, industry )

    elif suggestion_type == "Tailor to job description" :
        return tailor_to_job( text, industry, target_role )

    elif suggestion_type == "Fix formatting issues" :
        return fix_formatting( text )

    elif suggestion_type == "Enhance skills section" :
        return enhance_skills( text, industry )

    else :
        return ["Unknown suggestion type. Please select a valid option."]


def improve_bullet_points ( text: str, industry: str, target_role: str ) -> List[str] :
    """Improve bullet points to be more impactful"""

    prompt = f"""Transform these bullet points for a {target_role} resume in {industry}.

Original:
{text}

Provide 3 improved versions that:
1. Start with strong action verbs
2. Include quantifiable results
3. Show clear impact and value
4. Are concise and powerful

Format as numbered list."""

    response = generate_with_ai( prompt )

    # Parse response
    suggestions = []
    for line in response.split( '\n' ) :
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith( '-' ) or line.startswith( '•' )) :
            clean = line.lstrip( '0123456789.-•) ' ).strip()
            if clean :
                suggestions.append( clean )

    return suggestions[:3] if suggestions else [
        "Led cross-functional team of 8 to deliver project 20% under budget",
        "Increased efficiency by 40% through process automation and optimization",
        "Reduced costs by $150K annually while improving quality metrics by 25%"
    ]


def add_action_verbs ( text: str, target_role: str ) -> List[str] :
    """Suggest strong action verbs"""

    # Determine which categories are most relevant
    all_verbs = []
    for category, verbs in ACTION_VERB_CATEGORIES.items() :
        all_verbs.extend( verbs )

    suggestions = [
        f"Replace 'Responsible for' with '{all_verbs[0]}' or '{all_verbs[1]}'",
        f"Instead of 'Worked on', use '{all_verbs[2]}' or '{all_verbs[3]}'",
        f"Change 'Helped with' to '{all_verbs[4]}' or '{all_verbs[5]}'",
        f"Consider starting points with: {', '.join( all_verbs[6 :10] )}",
        f"Strong leadership verbs: {', '.join( ACTION_VERB_CATEGORIES['Leadership'][:3] )}"
    ]

    return suggestions


def quantify_achievements ( text: str, industry: str ) -> List[str] :
    """Suggest ways to add quantifiable metrics"""

    prompt = f"""Add quantifiable metrics to these achievements for {industry} industry:

Original:
{text}

Provide 3 versions with specific numbers, percentages, or metrics. Show measurable impact.
Examples: "increased by X%", "reduced costs by $X", "managed team of X", "served X clients"

Format as numbered list."""

    response = generate_with_ai( prompt )

    # Parse response
    suggestions = []
    for line in response.split( '\n' ) :
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith( '-' ) or line.startswith( '•' )) :
            clean = line.lstrip( '0123456789.-•) ' ).strip()
            if clean :
                suggestions.append( clean )

    return suggestions[:3] if suggestions else [
        "Managed portfolio of 50+ client accounts worth $2M+ in annual revenue",
        "Reduced processing time by 45% through automation, saving 15 hours per week",
        "Trained and mentored 12 team members, improving team productivity by 30%"
    ]


def tailor_to_job ( text: str, industry: str, target_role: str ) -> List[str] :
    """Tailor content to match job description"""

    prompt = f"""This is a job description or requirement for a {target_role} position:

{text}

Provide 5 resume bullet points that demonstrate relevant experience and skills.
Match the language and keywords from the description.
Show how you meet these requirements with specific examples.

Format as numbered list."""

    response = generate_with_ai( prompt )

    # Parse response
    suggestions = []
    for line in response.split( '\n' ) :
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith( '-' ) or line.startswith( '•' )) :
            clean = line.lstrip( '0123456789.-•) ' ).strip()
            if clean :
                suggestions.append( clean )

    return suggestions[:5] if suggestions else [
        "Align your experience with the specific requirements mentioned in the job posting",
        "Use exact keywords from the job description naturally in your bullet points",
        "Highlight relevant technical skills and tools mentioned in the posting",
        "Emphasize achievements that match the role's key responsibilities",
        "Mirror the language and terminology used by the company"
    ]


def fix_formatting ( text: str ) -> List[str] :
    """Suggest formatting improvements"""

    suggestions = [
        "Use consistent bullet points (• or -) throughout your resume",
        "Keep margins at 0.5-1 inch on all sides for readability",
        "Use a professional font like Arial, Calibri, or Times New Roman at 10-12pt",
        "Ensure consistent spacing between sections (typically 1-2 blank lines)",
        "Bold section headers and company names for visual hierarchy",
        "Align dates consistently (right-aligned is standard)",
        "Remove any tables, text boxes, or images that ATS can't read",
        "Use standard section headers: EXPERIENCE, EDUCATION, SKILLS"
    ]

    return suggestions


def enhance_skills ( text: str, industry: str ) -> List[str] :
    """Enhance skills section"""

    # Industry-specific skill suggestions
    skills_by_industry = {
        "technology" : [
            "Programming Languages: Python, Java, JavaScript, SQL, C++",
            "Frameworks & Tools: React, Django, Spring Boot, Docker, Kubernetes",
            "Cloud Platforms: AWS (EC2, S3, Lambda), Azure, Google Cloud",
            "Methodologies: Agile/Scrum, DevOps, CI/CD, Test-Driven Development"
        ],
        "finance" : [
            "Technical: Excel (Advanced), SQL, Python, R, Bloomberg Terminal",
            "Analysis: Financial Modeling, DCF Valuation, Forecasting, Risk Analysis",
            "Certifications: CFA, CPA, FRM (if applicable)",
            "Software: SAP, QuickBooks, Tableau, Power BI"
        ],
        "marketing" : [
            "Digital: SEO/SEM, Google Analytics, Social Media Marketing, Email Marketing",
            "Tools: HubSpot, Salesforce, Hootsuite, Mailchimp, Adobe Creative Suite",
            "Skills: Content Strategy, A/B Testing, Campaign Management, Brand Development",
            "Analytics: Google Analytics, Facebook Insights, Marketing Automation"
        ],
        "general" : [
            "Technical: Microsoft Office Suite (Excel, PowerPoint, Word), Google Workspace",
            "Communication: Written Communication, Presentation Skills, Public Speaking",
            "Organization: Project Management, Time Management, Multitasking",
            "Interpersonal: Team Collaboration, Customer Service, Problem Solving"
        ]
    }

    suggestions = skills_by_industry.get( industry, skills_by_industry["general"] )

    # Add general tips
    suggestions.extend( [
        "Organize skills by category (Technical, Soft Skills, Languages, etc.)",
        "List proficiency levels where relevant (Expert, Advanced, Intermediate)",
        "Include only skills relevant to your target role",
        "Add certifications and licenses in a separate section or within skills"
    ] )

    return suggestions