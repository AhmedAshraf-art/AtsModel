import spacy

nlp = spacy.load("en_core_web_sm")

def estimate_experience_from_level(level_word: str) -> str:
    level_map = {
        "junior": "0-1",
        "entry": "0-1",
        "mid": "2-4",
        "intermediate": "2-4",
        "senior": "3-5",
        "lead": "5+",
        "principal": "6+",
        "head": "6+"
    }
    for key in level_map:
        if key in level_word.lower():
            return level_map[key]
    return None

def parse_job_description(text: str) -> dict:
    doc = nlp(text)
    job_title = ""
    skills = []
    experience_years = None
    level = ""

    for sent in doc.sents:
        if "looking for" in sent.text.lower() or "we need" in sent.text.lower():
            job_title = sent.text.strip()
            break

    for token in doc:
        if token.pos_ in ["PROPN", "NOUN"] and token.is_alpha and token.text[0].isupper():
            skills.append(token.text)
        if token.text.lower() in ["junior", "senior", "mid", "entry", "lead", "principal", "head"]:
            level = token.text
            if not experience_years:
                experience_years = estimate_experience_from_level(level)

    for ent in doc.ents:
        if ent.label_ == "CARDINAL" and "year" in ent.sent.text.lower():
            experience_years = ent.text

    return {
        "title": job_title,
        "skills": list(set(skills)),
        "experience": experience_years,
        "level": level,
        "raw_text": text
    }
