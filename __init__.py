from .PerceptionNodeSuit.LLM import OpenAICompatibleConversation
from .PerceptionNodeSuit.Platforms.Gmail import Credentials, CheckMail, ThreadToOpenAIMessages, MarkAsRead, UpdateLabels, SendMail


def print_color_info(text, color='\033[92m'):
    CLEAR = '\033[0m'
    print(f"{color}{text}{CLEAR}")


print_color_info(f"### [START] 🤖💬 Perception Node Suit ###", "\033[1;35m")

NODE_CLASS_MAPPINGS = {
    "Credentials": Credentials.Credentials,
    "CheckEmail": CheckMail.CheckMail,
    # "Thread": Thread.Thread,
    "ThreadToOpenAIMessages": ThreadToOpenAIMessages.ThreadToOpenAIMessages,
    "MarkAsRead": MarkAsRead.MarkAsRead,
    "UpdateLabels": UpdateLabels.UpdateLabels,
    "SendEmail": SendMail.SendMail,
    "OpenAICompatibleConversation": OpenAICompatibleConversation.OpenAICompatibleConversation,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Credentials": "🤖💬 Perception: Gmail Credentials 🔐",
    "CheckEmail": "🤖💬 Perception: Gmail Checker 📨",
    # "Thread": "🤖💬 Perception: Gmail Thread 🧵",
    "ThreadToOpenAIMessages": "🤖💬 Perception: Gmail Thread To OpenAI Messages 🧵➡️🤖",
    "MarkAsRead": "🤖💬 Perception: Gmail Mark As Read ✅",
    "UpdateLabels": "🤖💬 Perception: Gmail Update Labels 🏷️",
    "SendEmail": "🤖💬 Perception: Gmail Send Mail 📩",
    "OpenAICompatibleConversation": "🤖💬 Perception: OpenAI Compatible Conversation 🫥💬",
}

WEB_DIRECTORY = "./Assets"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

print_color_info(f"### [END] 🤖💬 Perception Node Suit ###", "\033[1;35m")
