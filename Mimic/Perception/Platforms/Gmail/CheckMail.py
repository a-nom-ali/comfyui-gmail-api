import hashlib
import os.path

import numpy as np
import torch
from PIL import Image, ImageOps
import io

import folder_paths
from .Gmail import Gmail
import re


class CheckMail:
    RETURN_TYPES = (
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        [("IMAGE", "MASK", "INT")],
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
    OUTPUT_IS_LIST = (False, False, False, False, False, False, True, False, )

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
                        + Second value is a config for type "INT", "STRING" or "FLOAT".
        """
        return {
            "required": {
                "token_path": ("STRING", {"forceInput": True, "default": "token.json"}),
                "query": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "is:unread",
                    }),
            },
        }

    # @classmethod
    def IS_CHANGED(
            s,
            token_path: str,
            query: str):
        gmail = Gmail()

        if not gmail.authorize_with_token(token_path):
            raise Exception("Failed to authenticate with token")

        messages = gmail.get_messages(query)

        return messages[0]['id'] if messages is not None and len(messages) > 0 else None

    # @classmethod
    # def VALIDATE_INPUTS(
    #         s,
    #         token_path: str,
    #         query: str):
    #     m = hashlib.sha256()
    #     m.update()
    #     return m.hexdigest()

    def node(
            self,
            token_path: str,
            query: str):

        gmail = Gmail()

        if not gmail.authorize_with_token(token_path):
            raise Exception("Failed to authenticate with token")

        self.messages = gmail.get_messages(query)

        if self.messages is None or len(self.messages) == 0:
            return None, None, None, None, None, None, [], None,

        self.thread_id = self.messages[0]['threadId']
        self.message_id = self.messages[0]['id']

        # @classmethod
        # def IS_CHANGED(s, t_path, q, **kwargs):
        #     self.messages = gmail.get_messages(q)
        #     if self.messages and len(self.messages) > 0:
        #         self.message_id = self.messages[0]['id']
        #     return self.message_id
        #
        # setattr(self.__class__, 'IS_CHANGED', IS_CHANGED)

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
                self.attachments_to_images(self.messages[0]["attachments"]),
                token_path,
            )
            return self.result

        return None, None, None, None, None, None, [], None,

    def attachments_to_images(self, attachments:[]):
        images = []
        masks = []

        image_count = 0
        loaded_alpha = False
        zero_mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")

        for attachment in attachments:
            i = ImageOps.exif_transpose(Image.open(io.BytesIO(attachment["image"])))
            image = torch.from_numpy(
                np.array(
                    i.convert(
                        "RGB"))
                .astype(
                    np.float32)
                / 255.0)[None,]

            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
                if not loaded_alpha:
                    loaded_alpha = True
                    zero_mask = torch.zeros((len(image[0]), len(image[0][0])), dtype=torch.float32, device="cpu")
                    masks = [zero_mask] * image_count
            else:
                mask = zero_mask

            images.append(image)
            masks.append(mask)
            image_count += 1

        if len(images) == 0:
            return []

        return (torch.cat(images, dim=0), torch.stack(masks, dim=0), image_count)
