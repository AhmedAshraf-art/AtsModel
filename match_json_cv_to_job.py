import json
from extract_text_from_cv import flatten_cv_data
from parse_job_description import parse_job_description
from preprocess_text import preprocess
from embedding import get_embedding
from similarity import calculate_similarity
from experience_utils import calculate_experience_years, extract_years_from_text
from explain_mismatch import analyze_difference


def build_reason(score, explanation, exp_gap):
    reasons = []
    if explanation.get("missing_skills"):
        reasons.append("Missing skill(s): " + ", ".join(explanation["missing_skills"]))
    if not explanation.get("job_title_match"):
        reasons.append("Job title mismatch")
    if exp_gap is not None and exp_gap < 0:
        reasons.append(f"Experience is {abs(exp_gap)} year(s) less than required")
    return "; ".join(reasons) if reasons else "All criteria satisfied"


def match(cv_json_str: str, job_description_text: str) -> dict:
    try:
        cv_data = json.loads(cv_json_str)
        job_data = parse_job_description(job_description_text)

        cv_text = flatten_cv_data(cv_data)
        job_text = job_data.get("raw_text", "")

        clean_cv = preprocess(cv_text)
        clean_job = preprocess(job_text)

        cv_vec = get_embedding(clean_cv)
        job_vec = get_embedding(clean_job)

        score = calculate_similarity(cv_vec, job_vec)
        explanation = analyze_difference(cv_data, job_data)

        cv_exp = calculate_experience_years(cv_data) or extract_years_from_text(cv_text)
        job_exp = job_data.get("experience")

        exp_gap = None
        if job_exp and cv_exp:
            try:
                job_min_years = int(str(job_exp).split("-")[0].replace("+", ""))
                exp_gap = round(cv_exp - job_min_years, 1)
            except:
                pass

        return {
            "match_percentage": score or 0.0,
            "recommended": score >= 75 if score is not None else False,
            "job_title_matched": explanation.get("job_title_match", False),
            "matched_skills": explanation.get("matched_skills", []),
            "missing_skills": explanation.get("missing_skills", []),
            "experience_required": job_exp if job_exp else None,
            "cv_contains_experience": cv_exp if cv_exp else None,
            "experience_gap_years": exp_gap,
            "overall_status": (
                "Excellent match" if score and score >= 85 else
                "Good match" if score and score >= 70 else
                "Weak match" if score else "Unavailable"
            ),
            "reason": build_reason(score, explanation, exp_gap) if score else "Unable to process inputs"
        }

    except Exception as e:
        return {
            "match_percentage": 0.0,
            "recommended": False,
            "job_title_matched": False,
            "matched_skills": [],
            "missing_skills": [],
            "experience_required": None,
            "cv_contains_experience": None,
            "experience_gap_years": None,
            "overall_status": "Unavailable",
            "reason": f"Error occurred: {str(e)}"
        }
