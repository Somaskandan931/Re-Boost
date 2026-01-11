import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get OpenAI configuration from environment
api_key = os.getenv( "OPENAI_API_KEY" )
model_name = os.getenv( "OPENAI_MODEL", "gpt-3.5-turbo" )  # Default to gpt-3.5-turbo
org_id = os.getenv( "OPENAI_ORG_ID" )  # Optional organization ID

# Initialize OpenAI client
client = None

if not api_key :
    print( "⚠️  WARNING: OPENAI_API_KEY not found in environment variables" )
    print( "   AI features will use fallback mode. To enable AI:" )
    print( "   1. Copy .env.example to .env" )
    print( "   2. Add your OpenAI API key to the .env file" )
    print( "   3. Restart the application" )
else :
    try :
        from openai import OpenAI

        # Initialize client with optional organization ID
        client_args = {"api_key" : api_key}
        if org_id :
            client_args["organization"] = org_id

        client = OpenAI( **client_args )
        print( f"✅ OpenAI client initialized successfully" )
        print( f"   Model: {model_name}" )
        if org_id :
            print( f"   Organization: {org_id}" )

    except ImportError :
        print( "⚠️  OpenAI library not installed. Install with: pip install openai" )
        client = None
    except Exception as e :
        print( f"❌ Error initializing OpenAI client: {e}" )
        client = None

RESUME_SYSTEM_PROMPT = """You are an expert resume writer and career coach with 15+ years of experience.

Your expertise includes:
- Writing compelling, achievement-focused resume content
- Optimizing resumes for Applicant Tracking Systems (ATS)
- Tailoring content to specific industries and roles
- Using powerful action verbs and quantifiable metrics
- Creating impactful bullet points that showcase value

Guidelines:
- Be specific and actionable in your advice
- Focus on achievements over responsibilities
- Use strong action verbs (Led, Developed, Achieved, etc.)
- Include quantifiable metrics whenever possible
- Keep language professional but engaging
- Tailor advice to the specific industry and role
- Avoid generic phrases and clichés
"""


def generate_with_ai ( prompt: str, max_tokens: int = 800 ) -> str :
    """
    Generate text using OpenAI's GPT model.

    Args:
        prompt: The prompt to send to the AI
        max_tokens: Maximum tokens in response

    Returns:
        Generated text as string
    """

    if not client :
        # Fallback responses when no API key
        fallback_responses = {
            "analyze" : "This resume shows potential. Consider adding more quantifiable achievements and using stronger action verbs. Focus on demonstrating the impact of your work with specific metrics.",
            "improve" : "1. Start each bullet point with a strong action verb\n2. Add specific metrics and numbers\n3. Focus on achievements, not just responsibilities\n4. Use industry-specific keywords\n5. Keep bullet points concise and impactful",
            "optimize" : "Use standard section headers like EXPERIENCE, EDUCATION, and SKILLS. Include relevant keywords from the job description. Avoid tables, images, and complex formatting. Use simple bullet points.",
            "suggest" : "Consider these improvements:\n- Use stronger action verbs at the start of each point\n- Quantify your achievements with specific numbers\n- Focus on the impact and results of your work\n- Tailor your language to the industry standards",
            "extract" : '{"personal_info": {"name": "", "email": "", "phone": ""}, "education": [], "experience": [], "projects": [], "skills": [], "certifications": []}'
        }

        # Determine which fallback to use
        for key, response in fallback_responses.items() :
            if key in prompt.lower() :
                return response

        return "OpenAI API key not configured. Please add OPENAI_API_KEY to your .env file to enable AI-powered features. For now, you can still use the app with basic functionality."

    try :
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role" : "system", "content" : RESUME_SYSTEM_PROMPT},
                {"role" : "user", "content" : prompt}
            ],
            temperature=0.7,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content.strip()

    except Exception as e :
        print( f"❌ Error generating with AI: {e}" )

        # Check for common errors
        if "invalid_api_key" in str( e ) :
            return "Invalid OpenAI API key. Please check your .env file and ensure OPENAI_API_KEY is correct."
        elif "insufficient_quota" in str( e ) :
            return "OpenAI API quota exceeded. Please check your OpenAI account billing."
        elif "rate_limit" in str( e ) :
            return "OpenAI API rate limit reached. Please try again in a moment."
        else :
            return f"Error generating AI response: {str( e )}"


def check_api_status () -> dict :
    """
    Check if OpenAI API is configured and working.

    Returns:
        Dictionary with status information
    """
    status = {
        "configured" : bool( api_key ),
        "client_initialized" : bool( client ),
        "model" : model_name if client else None,
        "organization" : org_id if client and org_id else None
    }

    if client :
        try :
            # Test API with a simple request
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role" : "user", "content" : "test"}],
                max_tokens=5
            )
            status["working"] = True
            status["message"] = "OpenAI API is working correctly"
        except Exception as e :
            status["working"] = False
            status["message"] = f"OpenAI API error: {str( e )}"
    else :
        status["working"] = False
        status["message"] = "OpenAI API not configured"

    return status