from .Gmail import Gmail



class UpdateLabels:
    RETURN_TYPES = (
        "STRING",
        "STRING",
    )

    RETURN_NAMES = (
        "token_path",
        "message_id",
    )

    OUTPUT_NODE = True

    CATEGORY = "🤖💬 Perception/💌 Gmail"

    FUNCTION = "node"

    # OUTPUT_IS_LIST = (False, )

    def __init__(self):
        self.type = "output"
        self.result = None

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
                        + Secound value is a config for type "INT", "STRING" or "FLOAT".
        """
        return {
            "required": {
                "token_path": ("STRING", {"forceInput": True, "default": "credentials.json"}),
                "message_id": ("STRING", {"forceInput": True, "default": None}),
                "add_label_ids": ("STRING", {"default": None}),
                "remove_label_ids": ("STRING", {"default": "UNREAD"}),
            },
            # "hidden": {
            #     "changed": ("STRING", {"default": None}),
            # },
        }

    def node(
            self,
            token_path: str,
            message_id: str,
            add_label_ids=None,
            remove_label_ids="UNREAD"):

        if token_path is None or token_path.strip() == "" or token_path.strip() == "None":
            return (None, None, )

        gmail = Gmail()

        if not gmail.authorize_with_token(token_path):
            raise Exception("Failed to authenticate with token")

        if message_id:
            gmail.update_message_labels(message_id, add_label_ids.split(","), remove_label_ids.split(","))
            return (message_id, token_path, )
        else:
            return {"ui": {"result": "No Message Id"}}
