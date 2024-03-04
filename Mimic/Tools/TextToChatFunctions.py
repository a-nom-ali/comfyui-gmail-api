import json


class TextToChatFunctions:
    RETURN_TYPES = (
        "OPENAI_CHAT_FUNCTIONS",
    )

    RETURN_NAMES = (
        "functions",
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
                "text": ("STRING", {"default": "", "multiline": True}),
            }
        }

    def node(
            self,
            text: str):
        try:
            functions = json.loads(text.replace("/n", ""))
            return (functions if functions and len(functions) > 0 else None,)
        except json.decoder.JSONDecodeError as e:
            return {"ui": {"result":f"FUCK. Invalid JSON: {e}"}}
