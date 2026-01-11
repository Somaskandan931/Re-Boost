# AI Resume Booster - LaTeX Edition

A professional resume builder that generates high-quality LaTeX resumes with support for certificates, project links, GitHub integration, and multiple professional templates inspired by Overleaf.

## Key Features

### Professional LaTeX Templates
- **Modern Deedy**: Single-column modern design
- **Awesome CV**: Professional two-column layout
- **Tech Resume**: Developer-focused with emphasis on projects
- **Classic AltaCV**: Two-column with sidebar
- **Academic CV**: Traditional academic format
- **Minimalist**: Clean and simple design

### Comprehensive Resume Sections
- Personal Information with multiple contact methods
- Education with GPA and achievements
- Work Experience with detailed accomplishments
- Projects with GitHub and live demo links
- Technical Skills categorization
- Certifications with verification URLs
- Certificate file uploads (PDF/Images)
- Portfolio and social media links

### Advanced Features
- **Certificate Upload**: Upload and attach certification files
- **GitHub Integration**: Add project repositories and profiles
- **Live Demo Links**: Include project demonstrations
- **Resume Import**: Upload existing resumes (PDF/DOCX/TXT) for conversion
- **AI-Powered Extraction**: Automatically extract info from uploaded resumes
- **PDF Compilation**: Compile LaTeX to PDF directly (requires pdflatex)
- **Download LaTeX Source**: Get `.tex` file for Overleaf editing

## Quick Start

### Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **LaTeX Distribution** (optional, for PDF compilation):
  - Ubuntu/Debian: `sudo apt-get install texlive-full`
  - macOS: `brew install --cask mactex`
  - Windows: [Download MiKTeX](https://miktex.org/)

### Installation

1. **Clone or download the project**
```bash
git clone <repository-url>
cd resume-booster
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up OpenAI API (Optional)**

For AI-powered resume extraction and suggestions:

```bash
# Linux/Mac
export OPENAI_API_KEY='your-api-key-here'

# Windows
set OPENAI_API_KEY=your-api-key-here
```

*Note: The app works without an API key but with limited AI features.*

4. **Start the backend server**
```bash
uvicorn main:app --reload
```

5. **Start the Streamlit app** (in a new terminal)
```bash
streamlit run app.py
```

6. **Open your browser**
- Frontend UI: http://localhost:8501
- API Documentation: http://localhost:8000/docs

## Complete Usage Guide

### 1. Personal Information Tab

Enter your basic details:
- Full name, email, phone number
- Location (City, State)
- LinkedIn profile URL
- GitHub profile URL
- Portfolio/Personal website
- Professional summary

**Tip**: Make sure to include at least your email and one professional link (LinkedIn or GitHub).

### 2. Education & Certifications Tab

#### Add Education:
- Degree (B.S., M.S., Ph.D., etc.)
- Field of Study
- Institution name and location
- Graduation date
- GPA (optional but recommended if > 3.5)
- Relevant coursework or achievements

#### Add Certifications:
- Certification name
- Issuing organization
- Issue date
- Credential ID
- Verification URL
- **📎 Upload certificate file** (PDF, JPG, PNG)

**Example Certifications**:
- AWS Certified Solutions Architect
- Google Cloud Professional
- CFA Level I/II/III
- PMP Certification
- CompTIA Security+

### 3. Work Experience Tab

Add your professional experience with:
- Job title
- Company name and location
- Employment type (Full-time, Part-time, Internship, etc.)
- Start and end dates (use "Present" for current roles)
- Key achievements and responsibilities

**Writing Great Bullet Points**:
```
GOOD:
- Led team of 8 engineers to deliver microservices platform 3 weeks ahead of schedule
- Increased API performance by 60% through caching and optimization, serving 2M+ daily users
- Reduced infrastructure costs by $150K annually through AWS optimization

AVOID:
- Worked on various projects
- Responsible for backend development
- Helped with testing
```

### 4. Projects & Links Tab

#### Add Projects:
- Project name
- **GitHub repository URL** 
- **Live demo URL** 
- Technologies used
- Detailed description

**Example Projects**:
```
Project: E-Commerce Analytics Dashboard
GitHub: https://github.com/username/ecommerce-dashboard
Demo: https://demo.yoursite.com
Tech: React, Python, PostgreSQL, AWS
Description: Built real-time analytics dashboard processing 100K+ 
transactions daily with interactive visualizations
```

#### Technical Skills:
Add comma-separated skills:
```
Python, JavaScript, React, Node.js, AWS, Docker, Kubernetes, 
PostgreSQL, MongoDB, Git, CI/CD, Machine Learning, TensorFlow
```

### 5. Generate LaTeX Tab

1. **Select your preferred template** from the sidebar
2. **Choose your industry** (affects formatting emphasis)
3. **Click "Generate LaTeX Code"**
4. **Review the generated code**
5. **Download options**:
   - Download `.tex` file for Overleaf
   - Compile to PDF (if pdflatex installed)
   - Open in Overleaf

### 6. Upload Resume Tab

**Convert existing resumes to LaTeX**:

1. Upload your current resume (PDF, DOCX, or TXT)
2. Click "Extract & Convert to LaTeX"
3. AI extracts information automatically
4. Review and edit extracted data in other tabs
5. Generate LaTeX code

## Template Showcase

### Modern Deedy
- **Best for**: Software Engineers, Designers
- **Style**: Single column, modern, clean
- **Highlights**: Strong typography, clear sections

### Awesome CV
- **Best for**: Experienced Professionals
- **Style**: Professional two-column
- **Highlights**: Sidebar for skills, main column for experience

### Tech Resume
- **Best for**: Software Developers, Data Scientists
- **Style**: Developer-focused
- **Highlights**: Emphasis on projects and GitHub links

### Academic CV
- **Best for**: Researchers, PhD Candidates, Professors
- **Style**: Traditional academic format
- **Highlights**: Publications, research experience

## Project Structure

```
resume-booster/
├── app.py                          # Streamlit frontend
├── main.py                         # FastAPI backend
├── requirements.txt                # Dependencies
├── README.md                       # Documentation
│
├── backend/
│   ├── latex_generator.py         # LaTeX code generation
│   ├── resume_extractor.py        # Resume parsing & extraction
│   ├── llm.py                     # AI/LLM integration
│   ├── template_manager.py        # Template handling
│   └── suggestion_engine.py       # Resume suggestions
│
└── simple_db/                      # Generated files
    └── templates.json             # Template database
```

## API Endpoints

### Main Endpoints

- `POST /generate-latex` - Generate LaTeX code from resume data
- `POST /compile-pdf` - Compile LaTeX code to PDF
- `POST /extract-resume` - Extract data from uploaded resume
- `GET /templates` - List available templates
- `POST /validate-resume` - Validate resume data
- `POST /optimize-resume` - Get optimization suggestions
- `GET /status` - Check system status

Full API documentation: http://localhost:8000/docs

## Best Practices

### Resume Content

1. **Quantify Everything**
   - Use numbers, percentages, dollar amounts
   - Example: "Increased sales by 35% ($2M)" vs "Increased sales"

2. **Use Action Verbs**
   - Led, Developed, Achieved, Implemented, Designed
   - Avoid: "Responsible for", "Worked on", "Helped with"

3. **Show Impact**
   - Focus on results, not just responsibilities
   - Include the "So what?" - why it mattered

4. **Be Specific**
   - Concrete details > vague claims
   - "Managed team of 5" > "Managed a team"

### LaTeX Tips

1. **Keep It Simple**
   - Don't overcomplicate formatting
   - Focus on content readability

2. **Consistent Style**
   - Use one template throughout
   - Keep formatting uniform

3. **Test Compilation**
   - Always compile before submitting
   - Check for formatting issues

4. **ATS-Friendly**
   - Avoid excessive formatting
   - Use standard section headers
   - Keep fonts readable

### Links & Portfolios

1. **Always Include**:
   - LinkedIn profile
   - GitHub (for tech roles)
   - Portfolio website (if relevant)

2. **For Projects**:
   - Add GitHub repo links
   - Include live demos when possible
   - Ensure links work before sending

3. **For Certifications**:
   - Add verification URLs
   - Include credential IDs
   - Upload certificates when impressive

## Troubleshooting

### Backend Not Starting

```bash
# Check if port 8000 is in use
lsof -i :8000

# Use different port
uvicorn main:app --reload --port 8001
```

### Frontend Shows "Backend Offline"

1. Ensure backend is running: `uvicorn main:app --reload`
2. Check if accessible: http://127.0.0.1:8000
3. Look for errors in backend terminal

### PDF Compilation Fails

1. **Install LaTeX**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install texlive-full
   
   # macOS
   brew install --cask mactex
   
   # Windows
   # Download from https://miktex.org/
   ```

2. **Verify installation**:
   ```bash
   pdflatex --version
   ```

3. **Alternative**: Download `.tex` file and compile in [Overleaf](https://www.overleaf.com)

### Resume Extraction Not Working

1. **Enable AI features**: Set OPENAI_API_KEY
2. **Check file format**: Must be PDF, DOCX, or TXT
3. **File size**: Keep under 10MB
4. **Review extracted data**: Edit in respective tabs

### LaTeX Compilation Errors

Common issues:
- **Missing packages**: Use Overleaf (has all packages)
- **Special characters**: Automatically escaped in code
- **Long URLs**: May need manual line breaks

## Privacy & Security

- **Local Processing**: All resume data stays on your machine
- **No Cloud Storage**: Information is not stored externally
- **Certificate Files**: Stored temporarily during session only
- **API Usage**: OpenAI API only used for extraction/suggestions (optional)

## Use Cases

### Students & Recent Graduates
- Use Academic or Modern Deedy template
- Emphasize education and projects
- Include coursework and academic achievements

### Software Engineers
- Use Tech Resume template
- Highlight GitHub projects
- Focus on technical skills and technologies

### Experienced Professionals
- Use Awesome CV template
- Emphasize quantified achievements
- Include leadership and management experience

### Career Changers
- Use Minimalist template
- Focus on transferable skills
- Highlight relevant projects and certifications

**Transform your resume into a professional LaTeX masterpiece!**
