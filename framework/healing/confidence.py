def is_confident(score, threshold=0.8):

    return score >= threshold


def confidence_percentage(score):

    return int(score * 100)