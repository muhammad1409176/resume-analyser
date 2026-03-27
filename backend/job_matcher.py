from typing import List, Dict

# define some mock job postings for simulation
JOB_POSTINGS = [
    {
        "title": "Software Developer",
        "requirements": ["python", "java", "git", "docker"],
        "description": "Develop software applications using Python and Java."
    },
    {
        "title": "Frontend Developer",
        "requirements": ["javascript", "react", "html", "css"],
        "description": "Build user interfaces with React and modern JavaScript."
    },
    {
        "title": "Data Analyst",
        "requirements": ["sql", "python", "data science"],
        "description": "Analyze datasets using SQL and Python."
    }
]


def find_job_matches(resume_skills: List[str]) -> List[Dict]:
    """Return a list of job postings with match percentages."""
    matches = []
    rset = set([s.lower() for s in resume_skills])
    for job in JOB_POSTINGS:
        req = set([s.lower() for s in job.get("requirements", [])])
        if not req:
            pct = 0
        else:
            pct = len(rset & req) / len(req) * 100
        matches.append({
            "job": job["title"],
            "match_percentage": round(pct, 1),
            "matched_skills": list(rset & req),
            "missing_skills": list(req - rset)
        })
    matches.sort(key=lambda x: x["match_percentage"], reverse=True)
    return matches


def match_job_skills(resume_skills: List[str], job_skills: List[str]) -> Dict:
    """Simple matching between resume and job skill lists for the /api/match endpoint."""
    rset = set([s.lower() for s in resume_skills])
    jset = set([s.lower() for s in job_skills])
    if not jset:
        pct = 0
    else:
        pct = len(rset & jset) / len(jset) * 100
    return {
        "matched_skills": list(rset & jset),
        "missing_skills": list(jset - rset),
        "match_percentage": round(pct, 1)
    }
