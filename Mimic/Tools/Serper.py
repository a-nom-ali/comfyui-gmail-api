import requests
import json
from ...Mimic.Perception.Settings import api_settings


class Serper:
    RETURN_TYPES = (
        "STRING",
    )

    RETURN_NAMES = (
        "results",
    )

    OUTPUT_NODE = True

    CATEGORY = "🤖💬 Perception/🛠️ Tools"

    FUNCTION = "node"

    # OUTPUT_IS_LIST = (False, )

    def __init__(self):
        self.type = "output"
        self.api_base, self.api_key, self.organization = api_settings("serper", "search")

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
                "query": ("STRING", {"default": "workflow automation"}),
                "max_results": ("INT", {"default": 1}),
            }
        }

    def node(self,
             query: str,
             max_results:int):
        req_data = {
            "q": query,
            # Uncomment and fill as necessary, similar to your original code.
            # "hl": "en",
            # "google_domain": "google.com",
            "num": max_results,
            # "page": 1,
            # Additional parameters...
        }

        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

        response = requests.post(self.api_base, data=json.dumps(req_data), headers=headers)

        if response.status_code != 200:
            return {"ui": {"result": f"Error: {response.text}"}}
        else:
            return (response.text,)
