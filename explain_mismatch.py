def analyze_difference(cv_data: dict, job_data: dict) -> dict:
    explanation = {
        "missing_skills": [],
        "matched_skills": [],
        "job_title_match": True
    }

    job_skills = set(job_data.get("skills", []))
    job_title = job_data.get("title", "").lower()

    cv_skills = set()
    programming = cv_data.get("programming", [])
    for prog in programming:
        for field in ["programmingSkills", "applications", "platforms", "techniques", "frameworks", "softSkills"]:
            cv_skills.update(prog.get(field, []))

    cv_title = programming[0].get("jobTitle", "").lower() if programming else ""

    explanation["missing_skills"] = list(job_skills - cv_skills)
    explanation["matched_skills"] = list(job_skills & cv_skills)
    explanation["job_title_match"] = job_title in cv_title or cv_title in job_title

    return explanation
