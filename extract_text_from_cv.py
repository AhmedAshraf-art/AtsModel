def flatten_cv_data(cv_data: dict) -> str:
    sections = []

    if "personality" in cv_data:
        sections += list(cv_data["personality"].values())
    if "socialLinks" in cv_data:
        sections += list(cv_data["socialLinks"].values())
    if "researcherLinks" in cv_data:
        sections += list(cv_data["researcherLinks"].values())
    if "jobIndentification" in cv_data:
        sections += list(cv_data["jobIndentification"].values())

    for lang in cv_data.get("languages", []):
        sections += list(lang.values())

    programming = cv_data.get("programming", [])
    for prog in programming:
        sections.append(prog.get("jobTitle", ""))
        for field in ["programmingSkills", "applications", "platforms", "techniques", "frameworks", "softSkills"]:
            sections += prog.get(field, [])

    for section in ["education", "experience", "courses", "objectives", "refre"]:
        for item in cv_data.get(section, []):
            sections += list(item.values())

    return " ".join([str(item) for item in sections if isinstance(item, str)])
