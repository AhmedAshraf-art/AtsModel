from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(vec1, vec2) -> float:
    similarity = cosine_similarity([vec1], [vec2])[0][0]
    return round(similarity * 100, 2)
