from framework.healing.candidate_finder import CandidateFinder
from framework.healing.similarity import calculate_similarity
from framework.healing.confidence import is_confident
from framework.healing.confidence import confidence_percentage


class HealingEngine:

    def __init__(self, driver):

        self.driver = driver
        self.candidate_finder = CandidateFinder(driver)

    def heal(
        self,
        expected_text,
        expected_tag,
        expected_type,
        expected_name,
        expected_class
    ):

        candidates = self.candidate_finder.find_candidates(
            expected_tag
        )

        best_candidate = None
        best_score = 0

        for candidate in candidates:

            actual_text = candidate.text
            actual_tag = candidate.tag_name
            actual_type = candidate.get_attribute("type")
            actual_name = candidate.get_attribute("name")
            actual_class = candidate.get_attribute("class")

            score = calculate_similarity(
                expected_text,
                actual_text,
                expected_tag,
                actual_tag,
                expected_type,
                actual_type,
                expected_name,
                actual_name,
                expected_class,
                actual_class
            )

            if score > best_score:

                best_score = score
                best_candidate = candidate

        if best_candidate and is_confident(best_score):

            return {
                "element": best_candidate,
                "confidence": confidence_percentage(best_score)
            }

        return None