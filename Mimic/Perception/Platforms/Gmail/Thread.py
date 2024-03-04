import re

import folder_paths
from .Gmail import Gmail



class Thread:
    RETURN_TYPES = (
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        ["Image"],
        "STRING",
    )

    RETURN_NAMES = (
        "message_id",
        "thread_id",
        "subject",
        "to_email",
        "from_email",
        "body",
        "attachments",
        "token_path"
    )

    # OUTPUT_NODE = True

    CATEGORY = "🤖💬 Perception/💌 Gmail"

    FUNCTION = "node"
    OUTPUT_IS_LIST = (False, False, False, False, False, False, True, False)

    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.result = None
        self.messages = None
        self.thread_id = None
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
                "token_path": ("STRING", {"forceInput": True, "default": "token.json"}),
                "filter": ("STRING", {"default": None}),
            },
            # "hidden": {
            #     "changed": ("STRING", {"default": None}),
            # },
        }

    """
        The node will always be re executed if any of the inputs change but
        this method can be used to force the node to execute again even when the inputs don't change.
        You can make this node return a number or a string. This value will be compared to the one returned the last time the node was
        executed, if it is different the node will be executed again.
        This method is used in the core repo for the LoadImage node where they return the image hash as a string, if the image hash
        changes between executions the LoadImage node is executed again.
    """

    def node(
            self,
            token_path: str,
            query):

        gmail = Gmail()
        if not gmail.authorize_with_token(token_path):
            raise Exception("Failed to authenticate with token")

        self.messages = gmail.get_messages(query)

        if self.messages is None or len(self.messages) == 0:
            return self.message_id, self.thread_id, "Subject", "To", "From", "Body", [],

        self.thread_id = self.messages[0]['threadId']
        self.message_id = self.messages[0]['id']

        @classmethod
        def IS_CHANGED(s, t_path, q, **kwargs):
            self.messages = gmail.get_messages(q)
            if self.messages and len(self.messages) > 0:
                self.message_id = self.messages[0]['id']
            return self.message_id

        setattr(self.__class__, 'IS_CHANGED', IS_CHANGED)
        print(f"check_mail: {self.message_id}")
        self.messages = gmail.process_messages(self.messages)
        if len(self.messages) > 0:
            self.result = (
                self.message_id,
                self.thread_id,
                self.messages[0]["subject"],
                self.messages[0]["to"],
                self.messages[0]["from"],
                re.sub('<[^<]+?>', '', self.messages[0]["body"]),
                [],
                token_path
            )
            return self.result

        return self.message_id, self.thread_id, "Subject", "To", "From", "Body", [], token_path
