#!/usr/bin/env python3
import os
from trial import generate_pdf

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
if __name__ == "__main__":
    
    # Format contact information
    contact_info = format_contact_info(
        address="123 Main Street\nAnytown, ST 12345\nCountry",
        phone="+1 234 567 8901",
        email="john.doe@example.com"
    )
    
    # Format personal information
    personal_info = format_personal_info(
        dob="01/01/1990",
        nationality="United States"
    )
    
    # Format platforms
    platforms = format_platforms(
        github="johndoe",
        linkedin="john-doe"
    )
    
    # Format languages
    languages = format_languages([
        ("English", "Native", "usa"),
        ("German", "Fluent", "germany"),
        ("French", "Intermediate", "france")
    ])
    
    # Format education
    education = format_education([
        ("2010 - 2014", "University of Example", [
            "Bachelor of Science in Computer Science",
            "GPA: 3.8/4.0",
            "Thesis: Example Topic"
        ]),
        ("2014 - 2016", "Example Tech Institute", [
            "Master of Science in Data Science",
            "GPA: 3.9/4.0",
            "Thesis: Advanced Example Topic"
        ])
    ])
    
    # Format work experience
    work_experience = format_work_experience([
        ("2016 - 2020", "Example Corp", [
            "Software Engineer",
            "Developed and maintained company website",
            "Led team of 5 developers"
        ]),
        ("2020 - Present", "Tech Innovations Inc", [
            "Senior Software Engineer",
            "Architect for cloud migration project"
"Senior Software Engineer",
            "Architect for cloud migration project",
            "Implemented CI/CD pipelines"
        ])
    ])
    
    # Format publications
    publications = format_publications([
        ("2018", "Introduction to Machine Learning Algorithms"),
        # ("2020", "Cloud Architecture for Modern Applications"),
        # ("2022", "The Future of Artificial Intelligence")
    ])
    
    # Format awards
    awards = format_awards([
        # ("2017", "Best New Developer Award"),
        ("2019", "Innovation Excellence Prize"),
        ("2021", "Tech Leadership Award")
    ])
    
    # Format memberships
    memberships = format_memberships([
        ("2015", "ACM (Association for Computing Machinery)", "Member"),
        # ("2018", "IEEE Computer Society", "Senior Member"),
        # ("2020", "Open Source Initiative", "Contributor")
    ])
    
    # Format skills
    skills = format_skills({
       "Languages": "Python, Java, JavaScript, C++",
        "AIML": "Machine Learning & Data Analysis",
        "Cloud":"Cloud Architecture (AWS, Azure, GCP)",
        "Devops":"DevOps & CI/CD",
        "Db":"Database Design & Optimization"
}    )
    
    # Prepare all replacements
    replacements = {
        "name": "John Doe",
        "summary": "Senior Software Engineer & Cloud Architect",
        "about":"this is something about me",
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
    # Generate the PDF
    generate_pdf("fillable_template.tex", replacements=replacements)