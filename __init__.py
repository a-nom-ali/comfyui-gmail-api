from .Mimic.Perception.LLM import OpenAICompatibleConversation
from .Mimic.Perception.Platforms.Gmail import Credentials, CheckMail, ThreadToOpenAIMessages, MarkAsRead, UpdateLabels, SendMail
from .Mimic.Tools import PowerShell, SaveTextToFile, Serper, TextToChatMessages, TextToJSON, TextToChatFunctions
from .Mimic.Tools.Selenium import OpenBrowser, InformationExtractor, CloseBrowser, Navigation, ExecuteScript, Cookies



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
    "PowerShell": PowerShell.PowerShell,
    "OpenBrowser": OpenBrowser.OpenBrowser,
    "InformationExtractor": InformationExtractor.InformationExtractor,
    "Navigation": Navigation.Navigation,
    "ExecuteScript": ExecuteScript.ExecuteScript,
    "Cookies": Cookies.Cookies,
    "CloseBrowser": CloseBrowser.CloseBrowser,
    "SaveTextToFile": SaveTextToFile.SaveTextToFile,
    "Serper": Serper.Serper,
    "TextToJSON": TextToJSON.TextToJSON,
    "TextToChatMessages": TextToChatMessages.TextToChatMessages,
    "TextToChatFunctions": TextToChatFunctions.TextToChatFunctions,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Credentials": "🤖💬 Mimic: Gmail Credentials 🔐",
    "CheckEmail": "🤖💬 Mimic: Gmail Checker 📨",
    # "Thread": "🤖💬 Mimic: Gmail Thread 🧵",
    "ThreadToOpenAIMessages": "🤖💬 Mimic: Gmail Thread To OpenAI Messages 🧵➡️🤖",
    "MarkAsRead": "🤖💬 Mimic: Gmail Mark As Read ✅",
    "UpdateLabels": "🤖💬 Mimic: Gmail Update Labels 🏷️",
    "SendEmail": "🤖💬 Mimic: Gmail Send Mail 📩",
    "OpenAICompatibleConversation": "🤖💬 Mimic: OpenAI Compatible Conversation 🫥💬",
    "PowerShell": "🤖💬 Mimic: PowerShell 💪🐚",
    "OpenBrowser": "🤖💬 Mimic: Open Browser 🕸️📂",
    "InformationExtractor": "🤖💬 Mimic: Browser Information Extractor ℹ️➡️",
    "Navigation": "🤖💬 Mimic: Browser Navigation ℹ️➡️",
    "ExecuteScript": "🤖💬 Mimic: Browser Execute Script 🏃📜",
    "Cookies": "🤖💬 Mimic: Browser Cookies 🍪🍪",
    "CloseBrowser": "🤖💬 Mimic: Close Browser 🕸️📁",
    "SaveTextToFile": "🤖💬 Mimic: Save Text To File ➡️💾",
    "Serper": "🤖💬 Mimic: Serper Search 🌐🔍",
    "TextToJSON": "🤖💬 Mimic: Text To JSON 🔤🔣",
    "TextToChatMessages": "🤖💬 Mimic: Text To Chat Messages 🔣💬",
    "TextToChatFunctions": "🤖💬 Mimic: Text To Chat Functions 🔣🗯️",
}

WEB_DIRECTORY = "./Assets"

print_color_info(f"### [END] 🤖💬 Perception Node Suit ###", "\033[1;35m")

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']