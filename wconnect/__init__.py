"""wconnect - Messaging library with Telegram and Slack integration."""

from .wfile import WFile
from .wmessage import WMessage
from .wtelegram import Wtelegram

__all__ = ["WFile", "WMessage", "Wtelegram"]
__version__ = "0.1.0"
