import re

from .Gmail import Gmail


class ThreadToOpenAIMessages():
    RETURN_TYPES = (
        "OPENAI_CHAT_MESSAGES", )

    RETURN_NAMES = (
        "messages",
    )

    OUTPUT_NODE = True

    CATEGORY = "🤖💬 Perception/💌 Gmail"

    FUNCTION = "node"

    OUTPUT_IS_LIST = (False, True, )

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
                        + Second value is a config for type "INT", "STRING" or "FLOAT".
        """
        return {
            "required": {
                "thread_id": ("STRING", {"forceInput": True, "default": None}),
                "assistant_email": ("STRING", {"forceInput": True, "default": None}),
                "user_email": ("STRING", {"forceInput": True, "default": None}),
                "token_path": ("STRING", {"forceInput": True, "default": "token.json"}),
            },
            # "hidden": {
            #     "changed": ("STRING", {"default": None}),
            # },
        }

    def node(
            self,
            thread_id: str,
            assistant_email: str,
            user_email: str,
            token_path: str):

        if token_path is None or token_path.strip() == "" or token_path.strip() == "None":
            return (None, )

        if token_path is None or token_path.strip() == "" or token_path.strip() == "None":
            return (None, None, )

        gmail = Gmail()

        if not gmail.authorize_with_token(token_path):
            raise Exception("Failed to authenticate with token")

        if thread_id is not None:
            # get thread
            messages = gmail.thread(thread_id)
            results = []
            if messages and len(messages) > 0:
                for message in gmail.process_messages(messages):
                    body = re.sub('<[^<]+?>', '', message["body"])
                    if not body.strip() == "":
                        results.append({
                            "role": "user" if message["from"].find(user_email) > -1 else "assistant",
                            "content": body
                        })
            return (results, )
        else:
            return {"ui": {"result": "No ThreadId"}}

