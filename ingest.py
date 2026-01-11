"""
Template ingestion script for Resume Booster.
Creates a database of resume templates, examples, and best practices
organized by industry and role.
"""
import os
import json
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
DB_DIR = BASE_DIR / "simple_db"
DB_FILE = DB_DIR / "templates.json"

def create_templates():
    """Create resume template database"""
    print("=" * 60)
    print("🚀 Resume Booster Template Creation")
    print("=" * 60)

    # Create directories
    DB_DIR.mkdir(exist_ok=True)
    TEMPLATES_DIR.mkdir(exist_ok=True)

    # Define templates by industry and role
    templates = []

    # Technology templates
    templates.extend([
        {
            "industry": "technology",
            "role": "Software Engineer",
            "template": """PROFESSIONAL SUMMARY
Results-driven Software Engineer with X years of experience developing scalable applications.

TECHNICAL SKILLS
Languages: Python, Java, JavaScript, SQL
Frameworks: React, Django, Spring Boot
Tools: Git, Docker, Kubernetes, AWS

EXPERIENCE
Senior Software Engineer | Company Name | 2020-Present
• Developed microservices architecture serving 1M+ daily active users
• Reduced API response time by 40% through optimization
• Led team of 5 engineers in agile development cycles

EDUCATION
Bachelor of Science in Computer Science | University Name | 2019""",
            "examples": [
                "Developed microservices architecture that improved system scalability by 300%",
                "Reduced database query time by 60% through index optimization and caching",
                "Led migration of legacy system to cloud infrastructure, cutting costs by $50K annually",
                "Implemented CI/CD pipeline that reduced deployment time from 2 hours to 15 minutes"
            ],
            "keywords": ["agile", "microservices", "cloud", "devops", "api", "scalability"]
        },
        {
            "industry": "technology",
            "role": "Data Scientist",
            "template": """PROFESSIONAL SUMMARY
Data Scientist with expertise in machine learning and statistical analysis.

TECHNICAL SKILLS
Languages: Python, R, SQL
ML/AI: TensorFlow, PyTorch, Scikit-learn
Tools: Jupyter, Tableau, AWS SageMaker

EXPERIENCE
Data Scientist | Company Name | 2020-Present
• Built predictive models achieving 92% accuracy
• Increased revenue by $2M through customer segmentation
• Automated data pipeline processing 10TB+ daily

EDUCATION
Master of Science in Data Science | University Name | 2020""",
            "examples": [
                "Developed machine learning model that increased prediction accuracy by 25%",
                "Created customer churn model that saved $1.5M in annual revenue",
                "Built recommendation engine that improved user engagement by 40%",
                "Automated ETL pipeline reducing data processing time by 70%"
            ],
            "keywords": ["machine learning", "python", "sql", "modeling", "analytics"]
        }
    ])

    # Finance templates
    templates.extend([
        {
            "industry": "finance",
            "role": "Financial Analyst",
            "template": """PROFESSIONAL SUMMARY
Detail-oriented Financial Analyst with X years of experience in financial modeling and analysis.

SKILLS
Financial Modeling | Forecasting | Excel | SQL | Bloomberg | Tableau

EXPERIENCE
Financial Analyst | Company Name | 2020-Present
• Developed financial models supporting $50M+ investment decisions
• Improved forecasting accuracy by 30% through enhanced methodologies
• Created automated reporting saving 20 hours monthly

EDUCATION
Bachelor of Science in Finance | University Name | 2019
CFA Level II Candidate""",
            "examples": [
                "Developed DCF models for M&A transactions valued at $100M+",
                "Improved budget forecasting accuracy from 75% to 92%",
                "Identified cost-saving opportunities worth $500K annually",
                "Automated financial reporting process, reducing errors by 85%"
            ],
            "keywords": ["financial modeling", "analysis", "forecasting", "excel", "bloomberg"]
        }
    ])

    # Marketing templates
    templates.extend([
        {
            "industry": "marketing",
            "role": "Digital Marketer",
            "template": """PROFESSIONAL SUMMARY
Creative Digital Marketer with proven track record of driving growth and engagement.

SKILLS
SEO/SEM | Google Analytics | Content Marketing | Social Media | Email Campaigns

EXPERIENCE
Digital Marketing Manager | Company Name | 2020-Present
• Increased organic traffic by 150% through SEO optimization
• Managed $500K annual advertising budget across channels
• Improved conversion rate by 45% through A/B testing

EDUCATION
Bachelor of Arts in Marketing | University Name | 2019""",
            "examples": [
                "Launched email campaign that generated $250K in revenue with 35% open rate",
                "Grew social media following from 5K to 50K in 12 months",
                "Increased website conversion rate by 60% through UX improvements",
                "Reduced customer acquisition cost by 40% through campaign optimization"
            ],
            "keywords": ["seo", "sem", "google analytics", "campaigns", "conversion"]
        }
    ])

    # Healthcare templates
    templates.extend([
        {
            "industry": "healthcare",
            "role": "Nurse",
            "template": """PROFESSIONAL SUMMARY
Compassionate Registered Nurse with X years of experience in patient care.

CERTIFICATIONS
RN License | BLS | ACLS | PALS

EXPERIENCE
Registered Nurse | Hospital Name | 2020-Present
• Provided care for 8-12 patients per shift in ICU setting
• Achieved 98% patient satisfaction score
• Mentored 5 new nurses during orientation

EDUCATION
Bachelor of Science in Nursing | University Name | 2019""",
            "examples": [
                "Provided exceptional patient care achieving 98% satisfaction rating",
                "Reduced medication errors by 50% through double-check protocols",
                "Trained 15+ new nurses on ICU procedures and best practices",
                "Implemented patient care protocols improving outcomes by 25%"
            ],
            "keywords": ["patient care", "clinical", "healthcare", "nursing", "medical"]
        }
    ])

    # General/Entry Level templates
    templates.extend([
        {
            "industry": "general",
            "role": "Administrative Assistant",
            "template": """PROFESSIONAL SUMMARY
Organized Administrative Assistant with strong communication and multitasking skills.

SKILLS
Microsoft Office Suite | Scheduling | Communication | Data Entry | Customer Service

EXPERIENCE
Administrative Assistant | Company Name | 2020-Present
• Managed calendar and scheduling for C-level executives
• Improved filing system reducing document retrieval time by 50%
• Coordinated 20+ company events annually

EDUCATION
Associate's Degree in Business Administration | College Name | 2019""",
            "examples": [
                "Managed executive calendars and coordinated 100+ meetings monthly",
                "Reduced office supply costs by 25% through vendor negotiations",
                "Implemented new filing system improving efficiency by 40%",
                "Coordinated company events for 200+ employees with 95% attendance"
            ],
            "keywords": ["administrative", "organization", "communication", "microsoft office"]
        }
    ])

    # Save to database
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(templates, f, indent=2, ensure_ascii=False)

        print(f"\n{'=' * 60}")
        print(f"✅ Successfully created template database: {DB_FILE}")
        print(f"📊 Total templates: {len(templates)}")
        print(f"{'=' * 60}\n")

        # Print summary
        industries = {}
        for template in templates:
            industry = template['industry']
            if industry not in industries:
                industries[industry] = []
            industries[industry].append(template['role'])

        print("📋 Templates by Industry:")
        for industry, roles in industries.items():
            print(f"\n  {industry.title()}:")
            for role in roles:
                print(f"    • {role}")

        print(f"\n{'=' * 60}\n")

    except Exception as e:
        print(f"\n❌ Error saving database: {e}")

if __name__ == "__main__":
    create_templates()