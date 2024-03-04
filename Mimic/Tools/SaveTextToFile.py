from selenium import webdriver
import subprocess


class SaveTextToFile:
    RETURN_TYPES = (
    )

    RETURN_NAMES = (
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
                "filepath": ("STRING", {"default": "output/file.txt"}),
                "text": ("STRING", {"forceInput": True, "default": ""}),
            }
        }

    def node(
            self,
            filepath: str,
            text: str):

        try:

            with open(filepath, "w") as f:
                f.write(text)
            return ()
        except subprocess.CalledProcessError as e:
            return {"ui": {"result" :f"An error occurred: {e.stderr}"}}
