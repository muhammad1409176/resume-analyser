from typing import Dict
import re

# ------------------ TEXT CLEANING ------------------

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text


# ------------------ DOMAIN SKILLS ------------------

DOMAIN_SKILLS = {
    "Software Engineering": [
        "python","java","javascript","react","node","html","css",
        "sql","mongodb","git","docker","aws","linux"
    ],
    "Accounting": [
        "tally","gst","tax","audit","finance","excel"
    ],
    "Marketing": [
        "seo","marketing","branding","ads","content","social media"
    ],
    "Human Resources": [
        "hr","recruitment","payroll","employee"
    ],
    "Business / Sales": [
        "sales","account","client","customer","revenue","business","crm","deals"
    ],
    "General": []
}


# ------------------ DOMAIN DETECTION ------------------

def detect_domain(text: str) -> str:
    scores = {key: 0 for key in DOMAIN_SKILLS.keys()}

    for domain, keywords in DOMAIN_SKILLS.items():
        for word in keywords:
            if word in text:
                scores[domain] += 1

    best_domain = max(scores, key=scores.get)

    if scores[best_domain] == 0:
        return "General"

    return best_domain


# ------------------ SKILL MATCHING ------------------

def find_skills(text: str, skills: list):
    found = []

    for skill in skills:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found.append(skill)
        elif skill in text:
            found.append(skill)

    return list(set(found))


# ------------------ MAIN ANALYZER ------------------

def analyze_skills(resume_text: str) -> Dict:

    if not resume_text or len(resume_text.split()) < 20:
        return {"error": "Resume text not clear"}

    text = clean_text(resume_text)

    # Detect domain
    domain = detect_domain(text)

    # Get skills
    domain_skills = DOMAIN_SKILLS.get(domain, [])

    # Match skills
    detected_skills = find_skills(text, domain_skills)
    missing_skills = [s for s in domain_skills if s not in detected_skills]

    # Score
    score = min(100, len(detected_skills) * 12)

    # ------------------ INSIGHTS ------------------

    strengths = []
    if detected_skills:
        strengths.append(f"Strong skills in {', '.join(detected_skills[:5])}")
    if score >= 70:
        strengths.append("Good overall profile")

    weaknesses = []
    if not detected_skills:
        weaknesses.append("No strong skills detected")
    if missing_skills:
        weaknesses.append(f"Missing skills: {', '.join(missing_skills[:5])}")
    if score < 50:
        weaknesses.append("Profile needs improvement")

    suggestions = []
    if missing_skills:
        suggestions.append(f"Learn: {', '.join(missing_skills[:5])}")

    if domain == "Software Engineering":
        suggestions.append("Build projects and upload to GitHub")

    if domain == "Business / Sales":
        suggestions.append("Highlight achievements and revenue impact")

    # ------------------ JOB ROLES ------------------

    job_roles_map = {
        "Software Engineering": [
            "Frontend Developer",
            "Backend Developer",
            "Full Stack Developer",
            "Software Engineer Intern"
        ],
        "Business / Sales": [
            "Sales Executive",
            "Business Development Associate",
            "Account Manager",
            "Customer Success Manager"
        ],
        "Marketing": [
            "Digital Marketing Executive",
            "SEO Specialist",
            "Social Media Manager"
        ],
        "Accounting": [
            "Accountant",
            "Financial Analyst",
            "Audit Associate"
        ],
        "Human Resources": [
            "HR Executive",
            "Recruiter",
            "Talent Acquisition Specialist"
        ],
        "General": [
            "Intern",
            "Trainee"
        ]
    }

    recommended_jobs = job_roles_map.get(domain, [])

    # ------------------ AI SUMMARY ------------------

    summary = ""

    if detected_skills:
        summary += f"This resume shows strong skills in {', '.join(detected_skills[:3])}. "

    if missing_skills:
        summary += f"However, it lacks important skills like {', '.join(missing_skills[:3])}. "

    if score >= 70:
        summary += "Overall, the profile is strong and job-ready."
    elif score >= 50:
        summary += "The profile is decent but needs improvement."
    else:
        summary += "The profile needs significant improvement to be competitive."

    # ------------------ FINAL OUTPUT ------------------

    return {
        "domain": domain,
        "resume_score": score,
        "detected_skills": detected_skills,
        "missing_skills": missing_skills[:5],
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
        "recommended_jobs": recommended_jobs,
        "summary": summary
    }