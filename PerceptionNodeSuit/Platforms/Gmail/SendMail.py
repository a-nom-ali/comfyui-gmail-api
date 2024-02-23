import folder_paths
from .Gmail import Gmail



class SendMail:
    RETURN_TYPES = (
        "STRING",
        "STRING",
        "STRING",
        "STRING",
    )

    RETURN_NAMES = (
        "original_message_id",
        "message_id",
        "thread_id",
        "token_path",
    )

    OUTPUT_NODE = True

    CATEGORY = "🤖💬 Perception/💌 Gmail"

    FUNCTION = "node"

    # OUTPUT_IS_LIST = ()

    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.result = None
        self.messages = None
        self.message_id = None

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
                "message_id": ("STRING", {"forceInput": True, "default": None}),
                "thread_id": ("STRING", {"forceInput": True, "default": None}),
                "subject": ("STRING", {"default": None}),
                "from_email": ("STRING", {"forceInput": True, "default": None}),
                "to_email": ("STRING", {"forceInput": True, "default": None}),
                "body": ("STRING", {"default": None}),
                "token_path": ("STRING", {"forceInput": True, "default": "token.json"}),
            },
            "optional": {
                "attachments": ("IMAGE",)
            },
            "hidden": {
                "extra_pnginfo": "EXTRA_PNGINFO",
            }
        }

    def node(
            self,
            message_id,
            thread_id,
            subject,
            from_email,
            to_email,
            body,
            token_path=None,
            attachments=None,
            extra_pnginfo=None):

        if token_path is None or token_path.strip() == "" or token_path.strip() == "None":
            return None, None, None, None

        if body is None or body.strip() == "":
            return None, None, None, None
        gmail = Gmail()

        if not gmail.authorize_with_token(token_path):
            raise Exception("Failed to authenticate with token")

        message = gmail.send_message(body, subject, to_email, from_email, attachments, thread_id, extra_pnginfo)

        return (
            message_id if message is not None else None,
            message["message"] if message is not None and "message" in message else None,
            thread_id,
            token_path, )
