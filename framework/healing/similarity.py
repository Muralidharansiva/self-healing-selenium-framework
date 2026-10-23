def normalize(value):

    if not value:
        return ""

    return value.strip().lower()


def calculate_similarity(
    expected_text,
    actual_text,
    expected_tag,
    actual_tag,
    expected_type,
    actual_type,
    expected_name,
    actual_name
):

    score = 0

    if normalize(expected_text) == normalize(actual_text):

        score += 0.40

    if normalize(expected_tag) == normalize(actual_tag):

        score += 0.20

    if normalize(expected_type) == normalize(actual_type):

        score += 0.15

    if normalize(expected_name) == normalize(actual_name):

        score += 0.25

    return score