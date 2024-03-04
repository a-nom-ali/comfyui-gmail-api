from flask import current_app
from selenium import webdriver
import subprocess

from selenium.webdriver.common.by import By


SELENIUM_BROWSER = {}


class OpenBrowser:

    RETURN_TYPES = (
        "STRING",
        "STRING",
        "STRING",
    )

    RETURN_NAMES = (
        "title",
        "body",
        "identifier",
    )

    OUTPUT_NODE = True

    CATEGORY = "🤖💬 Perception/🛠️ Tools"

    FUNCTION = "node"

    # OUTPUT_IS_LIST = (False, )

    def __init__(self):
        self.type = "output"

    @classmethod
    def INPUT_TYPES(self):
        """
            Return a dictionary which contains config for all input fields.
            Some types (string): "MODEL", "VAE", "CLIP", "CONDITIONING", "LATENT", "IMAGE", "INT", "STRING", "FLOAT".
            Input types "INT", "STRING" or "FLOAT" are special values for fields on the node.
            The type can be a list for selection.

            Returns: `dict`:
                - Key input_fields_group (`string`): Can be either required, hidden or optional. A node class must have property `required`
                - Value input_fields (`dict`): Contains input fields config:
                    * Key field_name (`string`): Name of a entry-point method's argument
                    * Value field_config (`tuple`):
                        + First value is a string indicate the type of field or a list for selection.
                        + Second value is a config for type "INT", "STRING" or "FLOAT".
        """
        return {
            "required": {
                "url": ("STRING", {"forceInput": True, "default": "http://selenium.dev/"}),
                "identifier": ("STRING", {"default": "selenium"}),
                "browser": (["Chrome", "Chromium", "Firefox", "Safari", "Edge"],),
            }
        }

    def node(
            self,
            url: str,
            identifier: str,
            browser: str):
        try:
            # client_id = current_app.get('client_id', 'default')
            # print(f"Client ID: {client_id}")

            # if client_id not in SELENIUM_BROWSER:
            #     SELENIUM_BROWSER[client_id] = {}

            if identifier not in SELENIUM_BROWSER:
                if browser == "Chrome":
                    b = webdriver.Chrome()
                elif browser == "Chromium" or browser == "Edge":
                    b = webdriver.ChromiumEdge()
                elif browser == "Firefox":
                    b = webdriver.Firefox()
                elif browser == "Firefox":
                    b = webdriver.Safari()
            else:
                b = SELENIUM_BROWSER[identifier]

            SELENIUM_BROWSER[identifier] = b

            b.get(url)

            title = b.title
            body = b.find_element(By.TAG_NAME, 'body').text

            return title, body, identifier,
        except subprocess.CalledProcessError as e:
            return {"ui": {"result" :f"An error occurred: {e.stderr}"}}
