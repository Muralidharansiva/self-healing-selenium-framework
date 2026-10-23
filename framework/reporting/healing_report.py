import json
import os


class HealingReport:

    def __init__(self):

        self.events = []

    def add_event(
        self,
        element_name,
        original_locator,
        healed_locator,
        confidence
    ):

        event = {
            "element": element_name,
            "original_locator": original_locator,
            "healed_locator": healed_locator,
            "confidence": confidence,
            "status": "HEALED"
        }

        self.events.append(event)

        self.save_report()

    def save_report(self):

        os.makedirs("reports", exist_ok=True)

        with open(
            "reports/healing_report.json",
            "w"
        ) as file:

            json.dump(
                self.events,
                file,
                indent=4
            )