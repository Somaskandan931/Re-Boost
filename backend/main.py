from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import subprocess
import tempfile
from pathlib import Path

from backend.latex_generator import generate_latex_code
from backend.resume_extractor import extract_from_pdf, extract_from_docx, extract_from_txt

app = FastAPI(title="AI Resume Booster - LaTeX Edition", version="2.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# REQUEST/RESPONSE MODELS
class ResumeData(BaseModel):
    personal_info: Dict[str, str] = {}
    education: List[Dict] = []
    experience: List[Dict] = []
    projects: List[Dict] = []
    skills: List[str] = []
    certifications: List[Dict] = []
    links: Dict[str, str] = {}


class GenerateLaTeXRequest(BaseModel):
    resume_data: Dict[str, Any]
    template: str
    industry: str = "Technology"


class CompilePDFRequest(BaseModel):
    latex_code: str


# HEALTH CHECK ENDPOINT
@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Resume Booster - LaTeX Edition",
        "version": "2.0",
        "message": "Backend is running! LaTeX generation enabled.",
        "features": [
            "LaTeX Code Generation",
            "PDF Compilation",
            "Resume Extraction",
            "Certificate Upload Support",
            "Project Links Integration"
        ]
    }


# GENERATE LATEX ENDPOINT
@app.post("/generate-latex")
def generate_latex(request: GenerateLaTeXRequest):
    """
    Generate LaTeX code from resume data.
    """
    print(f"\n{'=' * 60}")
    print(f"Generating LaTeX Resume")
    print(f"Template: {request.template}")
    print(f"Industry: {request.industry}")
    print(f"{'=' * 60}")

    try:
        latex_code = generate_latex_code(
            resume_data=request.resume_data,
            template_name=request.template,
            industry=request.industry
        )

        print(f"LaTeX code generated successfully ({len(latex_code)} characters)")

        return {
            "success": True,
            "latex_code": latex_code,
            "template": request.template,
            "message": "LaTeX code generated successfully"
        }

    except Exception as e:
        print(f"Error generating LaTeX: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# COMPILE PDF ENDPOINT
@app.post("/compile-pdf")
def compile_pdf(request: CompilePDFRequest):
    """
    Compile LaTeX code to PDF.
    Requires pdflatex to be installed on the system.
    """
    print(f"\n{'=' * 60}")
    print(f"Compiling LaTeX to PDF")
    print(f"{'=' * 60}")

    try:
        # Create temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            tex_file = Path(tmpdir) / "resume.tex"

            # Write LaTeX code to file
            tex_file.write_text(request.latex_code, encoding='utf-8')

            # Compile with pdflatex
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-output-directory', tmpdir, str(tex_file)],
                capture_output=True,
                text=True,
                timeout=30
            )

            pdf_file = Path(tmpdir) / "resume.pdf"

            if pdf_file.exists():
                print(f"PDF compiled successfully")
                pdf_content = pdf_file.read_bytes()

                return Response(
                    content=pdf_content,
                    media_type="application/pdf",
                    headers={
                        "Content-Disposition": "attachment; filename=resume.pdf"
                    }
                )
            else:
                print(f"PDF compilation failed")
                print(f"Output: {result.stdout}")
                print(f"Error: {result.stderr}")
                raise HTTPException(
                    status_code=500,
                    detail="PDF compilation failed. Make sure pdflatex is installed."
                )

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="PDF compilation timeout")
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="pdflatex not found. Please install TeX Live or MiKTeX."
        )
    except Exception as e:
        print(f"Error compiling PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# EXTRACT RESUME ENDPOINT
@app.post("/extract-resume")
async def extract_resume(file: UploadFile = File(...)):
    """
    Extract information from uploaded resume.
    """
    print(f"\n{'=' * 60}")
    print(f"Extracting resume from: {file.filename}")
    print(f"{'=' * 60}")

    try:
        # Read file content
        content = await file.read()

        # Determine file type and extract
        if file.filename.endswith('.pdf'):
            resume_data = extract_from_pdf(content)
        elif file.filename.endswith('.docx'):
            resume_data = extract_from_docx(content)
        elif file.filename.endswith('.txt'):
            resume_data = extract_from_txt(content)
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload PDF, DOCX, or TXT."
            )

        print(f"Resume extracted successfully")

        return {
            "success": True,
            "resume_data": resume_data,
            "message": "Resume information extracted successfully"
        }

    except Exception as e:
        print(f"Error extracting resume: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# GET AVAILABLE TEMPLATES ENDPOINT
@app.get("/templates")
def get_templates():
    """
    Get list of available LaTeX templates.
    """
    return {
        "templates": {
            "modern_deedy": {
                "name": "Modern Deedy",
                "description": "Single column, modern design",
                "best_for": "Software Engineers, Designers"
            },
            "awesome_cv": {
                "name": "Awesome CV",
                "description": "Professional two-column layout",
                "best_for": "Experienced Professionals"
            },
            "classic_altacv": {
                "name": "Classic AltaCV",
                "description": "Two column with sidebar",
                "best_for": "Creative Professionals"
            },
            "academic": {
                "name": "Academic CV",
                "description": "Traditional academic format",
                "best_for": "Researchers, Academics"
            },
            "tech_resume": {
                "name": "Tech Resume",
                "description": "Developer-focused layout",
                "best_for": "Software Developers"
            },
            "minimalist": {
                "name": "Minimalist",
                "description": "Clean and simple design",
                "best_for": "All Industries"
            }
        }
    }


# VALIDATE RESUME DATA ENDPOINT
@app.post("/validate-resume")
def validate_resume(resume_data: ResumeData):
    """
    Validate resume data and provide feedback.
    """
    issues = []
    warnings = []

    # Check personal info
    personal = resume_data.personal_info
    if not personal.get("name"):
        issues.append("Name is required")
    if not personal.get("email"):
        issues.append("Email is required")
    if not personal.get("phone") and not personal.get("linkedin"):
        warnings.append("Consider adding phone or LinkedIn for contact")

    # Check sections
    if not resume_data.education:
        warnings.append("No education entries found")
    if not resume_data.experience:
        warnings.append("No work experience found")
    if not resume_data.skills:
        warnings.append("No skills listed")

    # Check for links
    has_links = (
            personal.get("github") or
            personal.get("linkedin") or
            personal.get("website") or
            any(proj.get("github") for proj in resume_data.projects)
    )

    if not has_links:
        warnings.append("Consider adding GitHub, LinkedIn, or portfolio links")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "score": max(0, 100 - len(issues) * 20 - len(warnings) * 5)
    }


# STATUS ENDPOINT
@app.get("/status")
def get_status():
    """
    Check system status and capabilities.
    """
    # Check if pdflatex is available
    pdflatex_available = False
    try:
        subprocess.run(['pdflatex', '--version'], capture_output=True, timeout=5)
        pdflatex_available = True
    except:
        pass

    return {
        "status": "online",
        "latex_generation": "enabled",
        "pdf_compilation": "enabled" if pdflatex_available else "disabled",
        "resume_extraction": "enabled",
        "message": "All systems operational" if pdflatex_available else "PDF compilation requires pdflatex installation"
    }


if __name__ == "__main__":
    import uvicorn

    print("\nStarting AI Resume Booster - LaTeX Edition...")
    print("Features:")
    print("   * LaTeX Code Generation")
    print("   * PDF Compilation (requires pdflatex)")
    print("   * Resume Information Extraction")
    print("   * Certificate Upload Support")
    print("API: http://127.0.0.1:8000")
    print("Docs: http://127.0.0.1:8000/docs\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)