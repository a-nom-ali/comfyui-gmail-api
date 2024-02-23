from .OpenAIClient import OpenAIClient
from ..Settings import load_settings


class OpenAICompatibleConversation:

    @classmethod
    def INPUT_TYPES(s):
        all_settings = load_settings()
        available_apis = [a for a in all_settings['openai_compatible']]
        default_model = all_settings['openai_compatible']['default']['model']

        return {
            "required": {
                "api": (available_apis, {
                    "default": "default"
                }),
                "model": ("STRING", {
                    "default": default_model
                }),
                "temperature": ("FLOAT", {
                    "default": 1.0, "min": 0.0, "max": 2.0, "step": 0.01,
                }),
                "messages": ("OPENAI_CHAT_MESSAGES", ),
                "system_context": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
            },
            "optional": {
                "top_p": ("FLOAT", {
                    "default": 1.0, "min": 0.001, "max": 1.0, "step": 0.01,
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("RESPONSE",)
    FUNCTION = "node"
    CATEGORY = "🤖💬 Perception/💌 Gmail"

    def node(self, api: str, model: str, temperature: float | None = None, messages=[], system_context: str = "",
             top_p: float | None = None):
        if messages is None or len(messages) == 0:
            return (None,)

        response = OpenAIClient.complete(
            key=api,
            model=model,
            temperature=temperature,
            top_p=top_p,
            system_content=system_context,
            messages=messages)

        return (f'{response.choices[0].message.content}',)
