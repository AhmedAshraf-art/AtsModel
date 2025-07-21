from datetime import datetime
import re

def calculate_experience_years(cv_data: dict) -> float:
    total_months = 0
    for job in cv_data.get("experience", []):
        start = job.get("start_date")
        end = job.get("end_date")
        if start and end:
            try:
                start_date = datetime.strptime(start, "%Y-%m-%d")
                end_date = datetime.strptime(end, "%Y-%m-%d")
                months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
                total_months += months
            except:
                continue
    total_years = round(total_months / 12, 1)
    return total_years if total_years > 0 else None

def extract_years_from_text(text: str) -> int:
    matches = re.findall(r'(\\d+)\\s+year', text.lower())
    if matches:
        return int(matches[0])
    return None
