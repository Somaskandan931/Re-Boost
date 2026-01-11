import os
import json
from typing import Dict, List, Optional

# Determine base directory
BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) )
DB_DIR = os.path.join( BASE_DIR, "simple_db" )
DB_FILE = os.path.join( DB_DIR, "templates.json" )

print( "📋 Template Database:", DB_FILE )

_templates = None

"""
LaTeX Template Manager
Provides LaTeX template structures for different resume styles.
"""


def get_latex_template ( template_name: str ) -> str :
    """
    Get LaTeX template structure by name.

    Args:
        template_name: Name of the template (e.g., "modern_deedy", "awesome_cv")

    Returns:
        LaTeX template string
    """
    templates = {
        "modern_deedy" : """\\documentclass[letterpaper,11pt]{article}
\\usepackage[utf8]{inputenc}
\\usepackage{geometry}
\\usepackage{enumitem}
\\usepackage{hyperref}
\\usepackage{xcolor}

\\geometry{left=0.75in, right=0.75in, top=0.75in, bottom=0.75in}
\\setlength{\\parindent}{0pt}
\\pagestyle{empty}

\\definecolor{primary}{RGB}{33, 150, 243}
\\hypersetup{colorlinks=true, linkcolor=primary, urlcolor=primary}

\\begin{document}

% HEADER
{\\Huge \\textbf{{{name}}}}\\\\[5pt]
{email} \\textbar{} {phone} \\textbar{} {location}\\\\
{links}

\\vspace{10pt}

% SUMMARY
\\section*{Professional Summary}
{summary}

\\vspace{10pt}

% EXPERIENCE
\\section*{Experience}
{experience}

\\vspace{10pt}

% EDUCATION
\\section*{Education}
{education}

\\vspace{10pt}

% SKILLS
\\section*{Skills}
{skills}

\\vspace{10pt}

% PROJECTS
\\section*{Projects}
{projects}

\\end{document}""",

        "awesome_cv" : """\\documentclass[11pt,a4paper]{article}
\\usepackage[utf8]{inputenc}
\\usepackage{geometry}
\\usepackage{enumitem}
\\usepackage{hyperref}
\\usepackage{xcolor}
\\usepackage{multicol}

\\geometry{left=1in, right=1in, top=1in, bottom=1in}
\\setlength{\\parindent}{0pt}
\\pagestyle{empty}

\\definecolor{awesome}{RGB}{64, 64, 64}
\\hypersetup{colorlinks=true, linkcolor=awesome, urlcolor=awesome}

\\begin{document}

% HEADER
{\\LARGE \\textbf{{{name}}}}\\\\[3pt]
\\hrule
\\vspace{5pt}
{email} \\textbar{} {phone} \\textbar{} {location}\\\\
{links}

\\vspace{15pt}

\\begin{minipage}[t]{0.65\\textwidth}
    \\section*{Experience}
    {experience}

    \\vspace{10pt}

    \\section*{Projects}
    {projects}
\\end{minipage}
\\hfill
\\begin{minipage}[t]{0.3\\textwidth}
    \\section*{Education}
    {education}

    \\vspace{10pt}

    \\section*{Skills}
    {skills}
\\end{minipage}

\\end{document}""",

        "classic_altacv" : """\\documentclass[10pt,a4paper]{article}
\\usepackage[utf8]{inputenc}
\\usepackage{geometry}
\\usepackage{enumitem}
\\usepackage{hyperref}
\\usepackage{xcolor}
\\usepackage{tikz}

\\geometry{left=0.5in, right=0.5in, top=0.5in, bottom=0.5in}
\\setlength{\\parindent}{0pt}
\\pagestyle{empty}

\\definecolor{accent}{RGB}{0, 102, 204}
\\hypersetup{colorlinks=true, linkcolor=accent, urlcolor=accent}

\\begin{document}

\\begin{minipage}[t]{0.35\\textwidth}
    % SIDEBAR
    {\\Large \\textbf{{{name}}}}\\\\[5pt]
    \\textcolor{accent}{\\rule{\\linewidth}{2pt}}

    \\vspace{10pt}

    \\textbf{Contact}\\\\
    {email}\\\\
    {phone}\\\\
    {location}\\\\
    {links}

    \\vspace{15pt}

    \\textbf{Skills}\\\\
    {skills}

    \\vspace{15pt}

    \\textbf{Education}\\\\
    {education}
\\end{minipage}
\\hfill
\\begin{minipage}[t]{0.6\\textwidth}
    % MAIN CONTENT
    \\section*{Professional Summary}
    {summary}

    \\vspace{10pt}

    \\section*{Experience}
    {experience}

    \\vspace{10pt}

    \\section*{Projects}
    {projects}
\\end{minipage}

\\end{document}""",

        "academic" : """\\documentclass[11pt,a4paper]{article}
\\usepackage[utf8]{inputenc}
\\usepackage{geometry}
\\usepackage{enumitem}
\\usepackage{hyperref}

\\geometry{left=1in, right=1in, top=1in, bottom=1in}
\\setlength{\\parindent}{0pt}

\\begin{document}

\\begin{center}
{\\Large \\textbf{{{name}}}}\\\\[5pt]
{email} \\textbar{} {phone}\\\\
{location}\\\\
{links}
\\end{center}

\\vspace{15pt}

\\section*{Education}
{education}

\\vspace{10pt}

\\section*{Research Experience}
{experience}

\\vspace{10pt}

\\section*{Publications}
{projects}

\\vspace{10pt}

\\section*{Skills}
{skills}

\\vspace{10pt}

\\section*{Certifications}
{certifications}

\\end{document}""",

        "tech_resume" : """\\documentclass[letterpaper,11pt]{article}
\\usepackage[utf8]{inputenc}
\\usepackage{geometry}
\\usepackage{enumitem}
\\usepackage{hyperref}
\\usepackage{xcolor}

\\geometry{left=0.5in, right=0.5in, top=0.5in, bottom=0.5in}
\\setlength{\\parindent}{0pt}
\\pagestyle{empty}

\\definecolor{techblue}{RGB}{0, 119, 181}
\\hypersetup{colorlinks=true, linkcolor=techblue, urlcolor=techblue}

\\begin{document}

{\\LARGE \\textbf{{{name}}}}\\\\[3pt]
{email} \\textbar{} {phone} \\textbar{} {links}

\\vspace{10pt}

\\section*{\\textcolor{techblue}{Technical Skills}}
{skills}

\\vspace{10pt}

\\section*{\\textcolor{techblue}{Experience}}
{experience}

\\vspace{10pt}

\\section*{\\textcolor{techblue}{Projects}}
{projects}

\\vspace{10pt}

\\section*{\\textcolor{techblue}{Education}}
{education}

\\end{document}""",

        "minimalist" : """\\documentclass[11pt,a4paper]{article}
\\usepackage[utf8]{inputenc}
\\usepackage{geometry}
\\usepackage{enumitem}
\\usepackage{hyperref}

\\geometry{left=1in, right=1in, top=1in, bottom=1in}
\\setlength{\\parindent}{0pt}
\\pagestyle{empty}

\\hypersetup{colorlinks=true, linkcolor=black, urlcolor=black}

\\begin{document}

{\\Large {name}}\\\\[2pt]
{email} \\textbar{} {phone} \\textbar{} {location}\\\\
{links}

\\vspace{15pt}

\\textbf{Summary}\\\\
{summary}

\\vspace{10pt}

\\textbf{Experience}\\\\
{experience}

\\vspace{10pt}

\\textbf{Education}\\\\
{education}

\\vspace{10pt}

\\textbf{Skills}\\\\
{skills}

\\vspace{10pt}

\\textbf{Projects}\\\\
{projects}

\\end{document}"""
    }

    # Return requested template or default to modern_deedy
    return templates.get( template_name, templates["modern_deedy"] )