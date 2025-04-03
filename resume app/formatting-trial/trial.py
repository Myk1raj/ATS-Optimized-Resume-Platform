import os
import subprocess
import shutil
from io import BytesIO

def format_latex_list(items):
    """
    Converts a Python list into a LaTeX itemized list.
    """
    if not isinstance(items, list):
        return str(items)  # Convert non-list items to string
    
    # Use simple paragraphs instead of LaTeX itemize for safer handling
    return "\n\\smallspace\n".join([item for item in items])

def generate_pdf(latex_template, output_tex="output.tex", output_pdf="output.pdf", replacements={}):
    """
    Generates a PDF from a LaTeX template by replacing placeholders.

    :param latex_template: Path to the LaTeX template file
    :param output_tex: Output LaTeX file name
    :param output_pdf: Output PDF file name
    :param replacements: Dictionary of placeholders and their replacements
    """
    try:
        # Read the LaTeX template
        with open(latex_template, "r", encoding="utf-8") as file:
            latex_content = file.read()

        # Process replacements
        processed_replacements = {}
        for key, value in replacements.items():
            if isinstance(value, list):
                processed_replacements[key] = format_latex_list(value)
            else:
                processed_replacements[key] = str(value)

        # Replace placeholders
        for key, value in processed_replacements.items():
            # Use double curly braces in the template for placeholders
            placeholder = f"{{{{{key}}}}}"
            latex_content = latex_content.replace(placeholder, value)

        # Write the modified LaTeX content to a new file
        with open(output_tex, "w", encoding="utf-8") as file:
            file.write(latex_content)

        # Check if icons directory exists and create dummy icons if not
        icons_dir = "icons"
        if not os.path.exists(icons_dir):
            os.makedirs(icons_dir, exist_ok=True)
            
            # Create dummy phone icon
            with open(os.path.join(icons_dir, "phone.tex"), "w") as f:
                f.write("\\begin{tikzpicture}\n\\draw (0,0) circle (0.5);\n\\end{tikzpicture}")
            
            # Create dummy email icon
            with open(os.path.join(icons_dir, "email.tex"), "w") as f:
                f.write("\\begin{tikzpicture}\n\\draw (0,0) rectangle (1,0.7);\n\\end{tikzpicture}")

        # Compile the LaTeX file to PDF using pdflatex
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", output_tex], 
            capture_output=True, 
            text=True
        )
        
        # Run twice to resolve references if needed
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", output_tex], 
            capture_output=True, 
            text=True
        )

        # Check if PDF was created
        if not os.path.exists(output_pdf):
            print(f"❌ PDF generation failed. pdflatex output:\n{result.stdout}\n{result.stderr}")
            
            # Write log to a separate file for easier debugging
            with open("pdflatex_error.log", "w") as f:
                f.write(result.stdout)
                f.write(result.stderr)
            
            print("Error details written to pdflatex_error.log")
            return False

        # Clean auxiliary files
        for ext in [".aux", ".log", ".out"]:
            try:
                os.remove(output_tex.replace(".tex", ext))
            except FileNotFoundError:
                pass

        print(f"✅ PDF generated successfully: {output_pdf}")
        return True

    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        return False


# Helper function to format contact information
def format_contact_info(address, phone, email):
    contact = ""
    
    # Format address
    if address:
        address_lines = address.split('\n')
        contact += f"""
        \\multirow{{4}}{{*}}{{\\scalebox{{0.075}}{{\\input{{icons/address.tex}}}}}}
            & \\textbf{{Address}} \\\\
        """
        for line in address_lines:
            contact += f"    & {line} \\\\\n"
        contact += "    & \\smallspace\n\n"
    
    # Format phone
    if phone:
        contact += f"""
        \\multirow{{2}}{{*}}{{\\scalebox{{0.075}}{{\\input{{icons/phone.tex}}}}}}
            & \\textbf{{Phone}} \\\\
            & \\href{{tel:{phone.replace(' ', '').replace('-', '')}}}{{\\text{{{phone}}}}} \\\\
            & \\smallspace
        """
    
    # Format email
    if email:
        contact += f"""
        \\multirow{{2}}{{*}}{{\\scalebox{{0.075}}{{\\input{{icons/email.tex}}}}}}
            & \\textbf{{E-Mail}} \\\\
            & \\href{{mailto:{email}}}{{\\text{{{email}}}}} \\\\
            & \\largespace
        """
    
    return contact

# Helper function to format personal information
def format_personal_info(dob, nationality):
    personal = ""
    
    if dob:
        personal += f"""
        \\multirow{{2}}{{*}}{{\\scalebox{{0.075}}{{\\input{{icons/birthday.tex}}}}}}
            & \\textbf{{Date of Birth}} \\\\
            & {dob} \\\\
            & \\smallspace
        """
    
    if nationality:
        personal += f"""
        \\multirow{{2}}{{*}}{{\\scalebox{{0.075}}{{\\input{{icons/nationality.tex}}}}}}
            & \\textbf{{Nationality}} \\\\
            & {nationality} \\\\
            & \\largespace
        """
    
    return personal

# Helper function to format platforms
def format_platforms(github, linkedin):
    platforms = ""
    
    if github:
        platforms += f"""
        \\multirow{{2}}{{*}}{{\\scalebox{{0.075}}{{\\input{{icons/github.tex}}}}}}
            & \\textbf{{GitHub}} \\\\
            & \\href{{https://github.com/{github}}}{{{github}}} \\\\
            & \\smallspace
        """
    
    if linkedin:
        platforms += f"""
        \\multirow{{2}}{{*}}{{\\scalebox{{0.075}}{{\\input{{icons/linkedin.tex}}}}}}
            & \\textbf{{LinkedIn}} \\\\
            & \\href{{https://linkedin.com/in/{linkedin}}}{{{linkedin}}} \\\\
            & \\largespace
        """
    
    return platforms

# Helper function to format languages
def format_languages(languages):
    """
    Format languages with their proficiency levels
    languages: List of tuples (language, proficiency, country_code)
    """
    result = ""
    
    for language, proficiency, country_code in languages:
        result += f"""
        \\multirow{{2}}{{*}}{{\\scalebox{{0.075}}{{\\input{{flags/{country_code}.tex}}}}}}
            & \\textbf{{{language}}} \\\\
            & {proficiency} \\\\
            & \\smallspace
        """
    
    return result

# Helper function to format education
def format_education(education_list):
    """
    Format education entries
    education_list: List of tuples (period, institution, details)
    details: List of strings for each detail line
    """
    result = ""
    
    for period, institution, details in education_list:
        result += f"{period}\n    & \\textbf{{{institution}}} \\\\\n"
        
        for detail in details:
            result += f"    & {detail} \\\\\n"
        
        result += "    & \\smallspace\n\n"
    
    return result

# Helper function to format work experience
def format_work_experience(work_list):
    """
    Format work experience entries
    work_list: List of tuples (period, company, details)
    details: List of strings for each detail line
    """
    result = ""
    
    for period, company, details in work_list:
        result += f"{period}\n    & \\textbf{{{company}}} \\\\\n"
        
        for detail in details:
            result += f"    & {detail} \\\\\n"
        
        result += "    & \\smallspace\n\n"
    
    return result

# Helper function to format publications
def format_publications(publications_list):
    """
    Format publications
    publications_list: List of tuples (year, title)
    """
    result = ""
    
    for year, title in publications_list:
        result += f"{year}\n    & \\textbf{{{title}}} \\\\\n"
    
    result += "    & \\largespace\n\n"
    
    return result

# Helper function to format awards
def format_awards(awards_list):
    """
    Format awards
    awards_list: List of tuples (year, award_name)
    """
    result = ""
    
    for year, award in awards_list:
        result += f"{year}\n    & \\textbf{{{award}}} \\\\\n"
    
    result += "    & \\largespace\n\n"
    
    return result

# Helper function to format memberships
def format_memberships(memberships_list):
    """
    Format memberships
    memberships_list: List of tuples (year, organization, role)
    """
    result = ""
    
    for year, organization, role in memberships_list:
        result += f"{year}\n    & \\textbf{{{organization}}} \\\\\n"
        result += f"    & {role} \\\\\n"
    
    result += "    & \\largespace\n\n"
    
    return result

# Helper function to format skills
def format_skills(skills_list):
    """
    Format skills
    skills_list: List of strings
    """
    result = ""
    
    for domain,skill in skills_list.items():
        skill = skill.replace("&", "\\&")
        result += f"{domain}\n& \\textbf{{{skill}}} \\\\\n"
    result += "    & \\largespace\n\n"
    return result

# Example usage
def generate_resume_pdf(resume_data):
    """Generate a PDF from resume data"""

    # Format contact information
    contact_info = format_contact_info(
        **resume_data.get("contact_info", {}) #FIXME
    )
    
    # Format personal information
    personal_info = format_personal_info(
        **resume_data.get("personal_info",{})
    )
    
    # Format platforms
    platforms = format_platforms(
        **resume_data.get("platforms",{})
    )
    
    # Format languages
    languages = format_languages(
        resume_data.get('languages',[])
    )
    
    # Format education
    education = format_education(
        resume_data.get('education',[])

    )
    
    # Format work experience
    work_experience = format_work_experience(
        resume_data.get('work_experience',[])

    )
    
    # Format publications
    publications = format_publications(
        resume_data.get('publications',[])

    )
    
    # Format awards
    awards = format_awards(
        resume_data.get('awards',[])

    )
    
    # Format memberships
    memberships = format_memberships(
        resume_data.get('memberships',[])

    )
    
    # Format skills
    skills = format_skills(
        **resume_data.get("skills",{})

        )
    
    # Prepare all replacements
    replacements = {
        "name": resume_data.get("name",'N/A'),
        "summary": resume_data.get("summary",'N/A'),
        "about":resume_data.get("about",'N/A'),
        "contact_info": contact_info,
        "personal_info": personal_info,
        "platforms": platforms,
        "languages": languages,
        "education": education,
        "work_experience": work_experience,
        "publications": publications,
        "awards": awards,
        "memberships": memberships,
        "skills": skills,
        "image": 'images/image.tex'
    }

    # Generate the PDF file
    output_pdf = "output.pdf"
    success = generate_pdf("fillable_template.tex", output_pdf=output_pdf, replacements=replacements)

    if not success:
        return None  # Return None if PDF generation failed

    # Read the generated PDF into a BytesIO object
    pdf_bytes = BytesIO()
    with open(output_pdf, "rb") as pdf_file:
        pdf_bytes.write(pdf_file.read())

    # Seek to the start of the BytesIO object
    pdf_bytes.seek(0)

    return pdf_bytes