import html
import json
from datetime import datetime
from pathlib import Path

from framework.config.config_loader import ConfigLoader


class HealingReport:

    def __init__(self):

        config = ConfigLoader().get_report_config()

        self.json_path = Path(
            config["json_path"]
        )

        self.html_path = Path(
            config["html_path"]
        )

        self.screenshot_dir = Path(
            config["screenshot_dir"]
        )

        self.events = []
        self.current_test = ""

    def start_test(self, test_name):

        self.current_test = test_name

    def add_event(
        self,
        element_name,
        original_locator,
        healed_locator,
        confidence,
        status,
        screenshot=None
    ):

        event = {
            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),
            "test": self.current_test,
            "element": element_name,
            "original_locator": original_locator,
            "healed_locator": healed_locator,
            "confidence": confidence,
            "status": status,
            "screenshot": screenshot
        }

        self.events.append(event)

    def capture_screenshot(
        self,
        driver,
        element_name
    ):

        self.screenshot_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )

        safe_name = (
            element_name
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        file_name = (
            f"{timestamp}_{safe_name}.png"
        )

        screenshot_path = (
            self.screenshot_dir / file_name
        )

        driver.save_screenshot(
            str(screenshot_path)
        )

        return (
            Path("screenshots") / file_name
        ).as_posix()

    def save_report(self):

        self.json_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.html_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.json_path,
            "w"
        ) as file:

            json.dump(
                self.events,
                file,
                indent=4
            )

        self.save_html_report()

    def save_html_report(self):

        healed = sum(
            event["status"] == "HEALED"
            for event in self.events
        )

        ambiguous = sum(
            event["status"] == "AMBIGUOUS"
            for event in self.events
        )

        not_healed = sum(
            event["status"] == "NOT_HEALED"
            for event in self.events
        )

        rows = []

        for event in self.events:

            screenshot = ""

            if event["screenshot"]:

                screenshot = (
                    f'<a href="{html.escape(event["screenshot"])}">'
                    "View screenshot"
                    "</a>"
                )

            rows.append(
                "<tr>"
                f"<td>{html.escape(event['timestamp'])}</td>"
                f"<td>{html.escape(event['test'])}</td>"
                f"<td>{html.escape(event['element'])}</td>"
                f"<td>{html.escape(event['status'])}</td>"
                f"<td>{event['confidence']}%</td>"
                f"<td>{html.escape(str(event['original_locator']))}</td>"
                f"<td>{html.escape(str(event['healed_locator']))}</td>"
                f"<td>{screenshot}</td>"
                "</tr>"
            )

        report = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Self-Healing Test Report</title>

    <style>

        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
        }}

        .summary {{
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
        }}

        .card {{
            border: 1px solid #ddd;
            padding: 20px;
            min-width: 120px;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
        }}

        th, td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }}

        th {{
            background: #f2f2f2;
        }}

    </style>

</head>

<body>

    <h1>Self-Healing Test Report</h1>

    <div class="summary">

        <div class="card">
            <strong>Healed</strong>
            <p>{healed}</p>
        </div>

        <div class="card">
            <strong>Ambiguous</strong>
            <p>{ambiguous}</p>
        </div>

        <div class="card">
            <strong>Not Healed</strong>
            <p>{not_healed}</p>
        </div>

        <div class="card">
            <strong>Total</strong>
            <p>{len(self.events)}</p>
        </div>

    </div>

    <table>

        <tr>
            <th>Timestamp</th>
            <th>Test</th>
            <th>Element</th>
            <th>Status</th>
            <th>Confidence</th>
            <th>Original Locator</th>
            <th>Healed Locator</th>
            <th>Screenshot</th>
        </tr>

        {"".join(rows)}

    </table>

</body>
</html>
"""

        with open(
            self.html_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(report)