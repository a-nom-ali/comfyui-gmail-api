import subprocess


class PowerShell:
    RETURN_TYPES = (
        "STRING",
    )

    RETURN_NAMES = (
        "output",
    )

    OUTPUT_NODE = True

    CATEGORY = "🤖💬 Perception/💌 Gmail"

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
                "command": ("STRING", {"default": "dir", "multiline": True}),
            }
        }

    def node(
            self,
            command: str):
        """
        Execute a command in PowerShell from Python.

        :param command: The PowerShell command to execute as a string.
        :return: The output of the command as a string.
        """
        # Ensure the command is executed in PowerShell
        cmd = ['powershell', '-Command', command]

        # Execute the command and capture the output
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return (result.stdout,)
        except subprocess.CalledProcessError as e:
            return f"An error occurred: {e.stderr}"
