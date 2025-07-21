import spacy

nlp = spacy.load("en_core_web_sm")

def preprocess(text: str) -> str:
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)
