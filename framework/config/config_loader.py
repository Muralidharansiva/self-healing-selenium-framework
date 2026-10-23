from pathlib import Path

import yaml


class ConfigLoader:

    def __init__(self):

        root_path = Path(__file__).resolve().parents[2]

        config_path = root_path / "config" / "config.yaml"

        with open(
            config_path,
            "r"
        ) as file:

            self.config = yaml.safe_load(file)

    def get_browser_config(self):

        return self.config["browser"]

    def get_healing_config(self):

        return self.config["healing"]

    def get_report_config(self):

        return self.config["report"]