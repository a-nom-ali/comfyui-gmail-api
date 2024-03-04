import os
import pathlib

import yaml

DEFAULT_SETTINGS = {
    "perception": {
        "openai": {
            "organisation": "NO ORG",
            "api_key": "NO API KEY",
            "model": "gpt-3.5-turbo"
        },
        "openai_compatible": {
            "organisation": "NO ORG",
            "api_key": "NO API KEY",
            "api_base": 'http://localhost:8000/v1'
        },
    }
}


def load_settings():
    path = os.path.join(os.path.join(os.path.dirname(__file__), "../.."), "settings.yaml")
    file_path = pathlib.Path(path)
    if not file_path.exists():
        return DEFAULT_SETTINGS['perception']

    with open(path) as settings:
        the_yaml = yaml.safe_load(settings)

    return the_yaml['perception']


def api_settings(section: str = "openai", group: str = 'openai_compatible'):
    settings = load_settings()[group][section]
    return settings['api_base'], settings['api_key'], settings['organisation']
