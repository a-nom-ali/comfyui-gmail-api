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
                "max_tokens": ("INT", {
                    "default": 512, "min": 144, "max": 2096, "step": 1
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
                "functions": ("OPENAI_CHAT_FUNCTIONS", ),
                "top_p": ("FLOAT", {
                    "default": 1.0, "min": 0.001, "max": 1.0, "step": 0.01,
                }),
            }
        }

    RETURN_TYPES = (
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "RESPONSE",
        "JSON",
    )
    FUNCTION = "node"
    CATEGORY = "🤖💬 Perception/🦜 LLM"

    def node(self,
             api: str,
             model: str,
             max_tokens: int,
             temperature: float | None = None,
             messages=[],
             system_context: str = "",
             functions=[],
             top_p: float | None = None):

        if messages is None or len(messages) == 0:
            return (None,)

        if messages[-1]["content"].strip == "" or messages[-1]["content"].strip == "None":
            messages[-1]["content"] = "Please kick off the conversation?"

        response = OpenAIClient.complete(
            key=api,
            model=model,
            temperature=temperature,
            top_p=top_p,
            system_content=system_context,
            messages=messages,
            functions=functions,
            max_tokens=max_tokens,
        )

        return (f'{response.choices[0].message.content}', json.dumps(response.choices), )
