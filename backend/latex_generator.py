"""
LaTeX Resume Generator
Generates professional LaTeX code from resume data using various templates.
"""

def escape_latex(text: str) -> str:
    """Escape special LaTeX characters."""
    if not text:
        return ""

    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text

def generate_modern_deedy(resume_data: dict) -> str:
    """Generate Modern Deedy style LaTeX resume."""

    personal = resume_data.get("personal_info", {})
    education = resume_data.get("education", [])
    experience = resume_data.get("experience", [])
    projects = resume_data.get("projects", [])
    skills = resume_data.get("skills", [])
    certifications = resume_data.get("certifications", [])

    latex = r"""\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[margin=0.5in]{geometry}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-1pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-5pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-5pt}
}

\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

\begin{document}

"""

    # Header with name and contact
    name = escape_latex(personal.get("name", "Your Name"))
    latex += f"\\begin{{center}}\n"
    latex += f"    \\textbf{{\\Huge \\scshape {name}}} \\\\ \\vspace{{1pt}}\n"

    # Contact info
    contact_parts = []
    if personal.get("phone"):
        contact_parts.append(escape_latex(personal["phone"]))
    if personal.get("email"):
        contact_parts.append(f"\\href{{mailto:{escape_latex(personal['email'])}}}{{{escape_latex(personal['email'])}}}")
    if personal.get("linkedin"):
        linkedin_clean = personal["linkedin"].replace("https://", "").replace("www.", "")
        contact_parts.append(f"\\href{{{escape_latex(personal['linkedin'])}}}{{\\underline{{{escape_latex(linkedin_clean)}}}}}")
    if personal.get("github"):
        github_clean = personal["github"].replace("https://", "").replace("www.", "")
        contact_parts.append(f"\\href{{{escape_latex(personal['github'])}}}{{\\underline{{{escape_latex(github_clean)}}}}}")

    latex += f"    \\small {' $|$ '.join(contact_parts)}\n"
    latex += "\\end{center}\n\n"

    # Summary
    if personal.get("summary"):
        latex += "\\section{Professional Summary}\n"
        latex += f"\\small{{{escape_latex(personal['summary'])}}}\n\n"

    # Education
    if education:
        latex += "\\section{Education}\n"
        latex += "  \\resumeSubHeadingListStart\n"
        for edu in education:
            degree = escape_latex(edu.get("degree", ""))
            field = escape_latex(edu.get("field", ""))
            institution = escape_latex(edu.get("institution", ""))
            location = escape_latex(edu.get("location", ""))
            graduation = escape_latex(edu.get("graduation", ""))

            degree_field = f"{degree} in {field}" if field else degree
            latex += f"    \\resumeSubheading\n"
            latex += f"      {{{institution}}}{{{location}}}\n"
            latex += f"      {{{degree_field}}}{{{graduation}}}\n"

            if edu.get("gpa"):
                latex += f"      \\resumeItemListStart\n"
                latex += f"        \\resumeItem{{GPA: {escape_latex(edu['gpa'])}}}\n"
                latex += f"      \\resumeItemListEnd\n"

        latex += "  \\resumeSubHeadingListEnd\n\n"

    # Experience
    if experience:
        latex += "\\section{Experience}\n"
        latex += "  \\resumeSubHeadingListStart\n"
        for exp in experience:
            title = escape_latex(exp.get("title", ""))
            company = escape_latex(exp.get("company", ""))
            location = escape_latex(exp.get("location", ""))
            date_range = f"{escape_latex(exp.get('start_date', ''))} - {escape_latex(exp.get('end_date', ''))}"

            latex += f"    \\resumeSubheading\n"
            latex += f"      {{{title}}}{{{date_range}}}\n"
            latex += f"      {{{company}}}{{{location}}}\n"

            if exp.get("description"):
                latex += "      \\resumeItemListStart\n"
                bullets = exp["description"].strip().split('\n')
                for bullet in bullets:
                    bullet = bullet.strip().lstrip('•-* ')
                    if bullet:
                        latex += f"        \\resumeItem{{{escape_latex(bullet)}}}\n"
                latex += "      \\resumeItemListEnd\n"

        latex += "  \\resumeSubHeadingListEnd\n\n"

    # Projects
    if projects:
        latex += "\\section{Projects}\n"
        latex += "    \\resumeSubHeadingListStart\n"
        for proj in projects:
            name = escape_latex(proj.get("name", ""))
            tech = escape_latex(proj.get("technologies", ""))

            # Add project links if available
            links = []
            if proj.get("github"):
                links.append(f"\\href{{{escape_latex(proj['github'])}}}{{GitHub}}")
            if proj.get("demo"):
                links.append(f"\\href{{{escape_latex(proj['demo'])}}}{{Live Demo}}")

            link_str = f" | {' | '.join(links)}" if links else ""

            latex += f"      \\resumeProjectHeading\n"
            latex += f"          {{\\textbf{{{name}}} $|$ \\emph{{{tech}}}{link_str}{{}}\n"

            if proj.get("description"):
                latex += "          \\resumeItemListStart\n"
                latex += f"            \\resumeItem{{{escape_latex(proj['description'])}}}\n"
                latex += "          \\resumeItemListEnd\n"

        latex += "    \\resumeSubHeadingListEnd\n\n"

    # Technical Skills
    if skills:
        latex += "\\section{Technical Skills}\n"
        latex += " \\begin{itemize}[leftmargin=0.15in, label={}]\n"
        latex += "    \\small{\\item{\n"

        # Group skills
        skills_str = ", ".join([escape_latex(skill) for skill in skills])
        latex += f"     \\textbf{{Skills}}{{: {skills_str}}}\n"

        latex += "    }}\n"
        latex += " \\end{itemize}\n\n"

    # Certifications
    if certifications:
        latex += "\\section{Certifications}\n"
        latex += "  \\resumeSubHeadingListStart\n"
        for cert in certifications:
            name = escape_latex(cert.get("name", ""))
            issuer = escape_latex(cert.get("issuer", ""))
            date = escape_latex(cert.get("date", ""))

            cert_line = f"{name} - {issuer}"
            if cert.get("url"):
                cert_line = f"\\href{{{escape_latex(cert['url'])}}}{{{cert_line}}}"

            latex += f"    \\resumeSubheading{{{cert_line}}}{{{date}}}{{}}{{}} \n"

        latex += "  \\resumeSubHeadingListEnd\n\n"

    latex += "\\end{document}\n"

    return latex

def generate_tech_resume(resume_data: dict) -> str:
    """Generate tech-focused LaTeX resume."""

    personal = resume_data.get("personal_info", {})
    education = resume_data.get("education", [])
    experience = resume_data.get("experience", [])
    projects = resume_data.get("projects", [])
    skills = resume_data.get("skills", [])

    latex = r"""\documentclass[letterpaper,11pt]{article}

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{hyperref}
\usepackage{enumitem}
\usepackage{titlesec}

\geometry{left=0.75in,right=0.75in,top=0.75in,bottom=0.75in}

\titleformat{\section}{\large\bfseries}{}{0em}{}[\titlerule]
\titlespacing{\section}{0pt}{10pt}{5pt}

\setlist[itemize]{leftmargin=*,noitemsep,topsep=0pt}

\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    urlcolor=blue,
}

\begin{document}

\begin{center}
"""

    name = escape_latex(personal.get("name", "Your Name"))
    latex += f"    {{\\LARGE \\textbf{{{name}}}}} \\\\\n"
    latex += "    \\vspace{3pt}\n"

    # Contact line
    contact = []
    if personal.get("email"):
        contact.append(f"\\href{{mailto:{escape_latex(personal['email'])}}}{{{escape_latex(personal['email'])}}}")
    if personal.get("phone"):
        contact.append(escape_latex(personal["phone"]))
    if personal.get("github"):
        contact.append(f"\\href{{{escape_latex(personal['github'])}}}{{GitHub}}")
    if personal.get("linkedin"):
        contact.append(f"\\href{{{escape_latex(personal['linkedin'])}}}{{LinkedIn}}")
    if personal.get("website"):
        contact.append(f"\\href{{{escape_latex(personal['website'])}}}{{Portfolio}}")

    latex += f"    {' $|$ '.join(contact)}\n"
    latex += "\\end{center}\n\n"

    # Technical Skills first (for tech resume)
    if skills:
        latex += "\\section*{Technical Skills}\n"
        skills_str = ", ".join([escape_latex(s) for s in skills])
        latex += f"{skills_str}\n\n"

    # Experience
    if experience:
        latex += "\\section*{Experience}\n"
        for exp in experience:
            title = escape_latex(exp.get("title", ""))
            company = escape_latex(exp.get("company", ""))
            dates = f"{escape_latex(exp.get('start_date', ''))} - {escape_latex(exp.get('end_date', ''))}"

            latex += f"\\textbf{{{title}}} \\hfill {dates} \\\\\n"
            latex += f"\\textit{{{company}}} \\\\\n"

            if exp.get("description"):
                latex += "\\begin{itemize}\n"
                bullets = exp["description"].strip().split('\n')
                for bullet in bullets:
                    bullet = bullet.strip().lstrip('•-* ')
                    if bullet:
                        latex += f"    \\item {escape_latex(bullet)}\n"
                latex += "\\end{itemize}\n"
            latex += "\\vspace{5pt}\n\n"

    # Projects
    if projects:
        latex += "\\section*{Projects}\n"
        for proj in projects:
            name = escape_latex(proj.get("name", ""))
            tech = escape_latex(proj.get("technologies", ""))

            links = []
            if proj.get("github"):
                links.append(f"\\href{{{escape_latex(proj['github'])}}}{{GitHub}}")
            if proj.get("demo"):
                links.append(f"\\href{{{escape_latex(proj['demo'])}}}{{Demo}}")

            link_str = f" | {' | '.join(links)}" if links else ""

            latex += f"\\textbf{{{name}}} | {tech}{link_str} \\\\\n"
            if proj.get("description"):
                latex += f"{escape_latex(proj['description'])}\n"
            latex += "\\vspace{5pt}\n\n"

    # Education
    if education:
        latex += "\\section*{Education}\n"
        for edu in education:
            degree = escape_latex(edu.get("degree", ""))
            field = escape_latex(edu.get("field", ""))
            institution = escape_latex(edu.get("institution", ""))
            graduation = escape_latex(edu.get("graduation", ""))

            latex += f"\\textbf{{{degree}}} in {field} \\hfill {graduation} \\\\\n"
            latex += f"{institution}"
            if edu.get("gpa"):
                latex += f" | GPA: {escape_latex(edu['gpa'])}"
            latex += " \\\\\n\n"

    latex += "\\end{document}\n"

    return latex

def generate_latex_code(resume_data: dict, template_name: str, industry: str = "Technology") -> str:
    """
    Main function to generate LaTeX code based on template.
    """

    if template_name == "tech_resume":
        return generate_tech_resume(resume_data)
    elif template_name in ["modern_deedy", "awesome_cv", "classic_altacv"]:
        return generate_modern_deedy(resume_data)
    elif template_name == "minimalist":
        return generate_tech_resume(resume_data)  # Use tech resume for minimalist
    elif template_name == "academic":
        return generate_modern_deedy(resume_data)  # Can create academic variant
    else:
        # Default to modern_deedy
        return generate_modern_deedy(resume_data)