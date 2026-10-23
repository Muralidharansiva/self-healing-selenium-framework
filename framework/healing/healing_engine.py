from framework.config.config_loader import ConfigLoader
from framework.healing.candidate_finder import CandidateFinder
from framework.healing.similarity import calculate_similarity
from framework.healing.confidence import is_confident
from framework.healing.confidence import confidence_percentage


class HealingEngine:

    def __init__(self, driver):

        self.driver = driver
        self.candidate_finder = CandidateFinder(driver)

        config = ConfigLoader().get_healing_config()

        self.confidence_threshold = config[
            "confidence_threshold"
        ]

        self.ambiguity_margin = config[
            "ambiguity_margin"
        ]

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

        scored_candidates = []

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

            scored_candidates.append(
                (
                    candidate,
                    score
                )
            )

        scored_candidates.sort(
            key=lambda item: item[1],
            reverse=True
        )

        if not scored_candidates:

            return {
                "status": "NOT_HEALED",
                "element": None,
                "confidence": 0
            }

        best_candidate = scored_candidates[0][0]
        best_score = scored_candidates[0][1]

        best_confidence = confidence_percentage(
            best_score
        )

        if not is_confident(
            best_score,
            self.confidence_threshold
        ):

            return {
                "status": "NOT_HEALED",
                "element": None,
                "confidence": best_confidence
            }

        if len(scored_candidates) > 1:

            second_score = scored_candidates[1][1]

            if is_confident(
                second_score,
                self.confidence_threshold
            ):

                score_difference = (
                    best_score - second_score
                )

                if score_difference <= self.ambiguity_margin:

                    return {
                        "status": "AMBIGUOUS",
                        "element": None,
                        "confidence": best_confidence
                    }

        return {
            "status": "HEALED",
            "element": best_candidate,
            "confidence": best_confidence
        }