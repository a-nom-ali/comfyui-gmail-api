from flask import current_app
from selenium.webdriver.common.by import By

from .OpenBrowser import SELENIUM_BROWSER


class InformationExtractor:
    RETURN_TYPES = (
        "STRING",
        "STRING",
    )

    RETURN_NAMES = (
        "identifier",
        "text",
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
        bys = [
            By.ID,
            By.XPATH,
            By.LINK_TEXT,
            By.PARTIAL_LINK_TEXT,
            By.NAME,
            By.TAG_NAME,
            By.CLASS_NAME,
            By.CSS_SELECTOR
        ]
        return {
            "required": {
                "identifier": ("STRING", {"forceInput": True, "default": None}),
                "by": (bys, {"default": By.TAG_NAME}),
                "query": ("STRING", {"default": "p"}),
            }
        }

    def node(
            self,
            identifier: str,
            by: str,
            query: str):

        try:
            if identifier in SELENIUM_BROWSER:
                browser = SELENIUM_BROWSER[identifier]
                return (identifier, browser.find_element(by, query).text,)
            else:
                return {"ui": {"result": f"No browser with identifier {identifier}"}}

        except Exception as e:
            return {"ui": {"result": f"An error occurred: {e.stderr}"}}
