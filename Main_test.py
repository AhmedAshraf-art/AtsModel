import json
from match_json_cv_to_job import match

cv_json = '''{
  "personality": {
    "first_name": "Sarah",
    "last_name": "Mahmoud",
    "email": "sarah.dev@example.com",
    "phone": "01012345678",
    "address": "Cairo, Egypt",
    "birthday": "1995-05-10"
  },
  "jobIndentification": {
    "categoryId": "dev-backend",
    "jobTitle": "Backend Developer"
  },
  "experience": [
    {
      "job_title": "Backend Developer",
      "company": "XYZ Solutions",
      "start_date": "2019-01-01",
      "end_date": "2023-01-01",
      "description": "Developed and maintained REST APIs using Django and PostgreSQL."
    }
  ],
  "education": [
    {
      "degree": "B.Sc. in Computer Science",
      "institution": "Cairo University",
      "graduation_year": "2017"
    }
  ],
  "programming": [
    {
      "jobTitle": "Backend Developer",
      "programmingSkills": ["Python", "Django", "SQL", "Git"],
      "applications": ["Postman"],
      "platforms": ["Linux"],
      "techniques": ["REST APIs", "Database Design"],
      "frameworks": ["Django", "Flask"],
      "softSkills": ["Teamwork", "Problem Solving"]
    }
  ]
}'''

job_description = """
We are looking for a Senior Backend Developer with at least 3 years of experience in Python and Django.

The candidate should be familiar with SQL databases, Git version control, and RESTful API development. Knowledge of Docker and PostgreSQL is a plus.

Strong communication skills and ability to work in a team are required.
"""

def convert(o):
    import numpy as np
    if isinstance(o, (np.float32, np.float64)):
        return float(o)
    if isinstance(o, (np.int32, np.int64)):
        return int(o)
    return str(o)

if __name__ == "__main__":
    result = match(cv_json, job_description)
    print(json.dumps(result, indent=4, default=convert))
