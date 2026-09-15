"""Example: Text Message Sender.

Demonstrates sending text messages to Telegram users.
"""

import os
from typing import Union

from wconnect import Wtelegram

if "TELEGRAM_BOT_TOKEN" not in os.environ:
    os.environ["TELEGRAM_BOT_TOKEN"] = "8823336064:AAE2sky0B4vOD5_z2cKsDekv4T9LSKiSlGA"

DEFAULT_CHAT_ID = "6586101740"


def send_text_notification(
    chat_id: Union[int, str],
    message: str,
) -> bool:
    """Send a text notification to a Telegram user/chat."""
    with Wtelegram() as producer:
        success = producer.send(to=chat_id, message=message)
        if success:
            print(f"[SUCCESS] Text message delivered to {chat_id}")
        else:
            print(f"[ERROR] Failed to deliver text message to {chat_id}")
        return success


def main() -> None:
    """Execute text sender workflow."""
    print("=== Text Message Sender ===")
    send_text_notification(
        chat_id=DEFAULT_CHAT_ID,
        message="✅ Hello! This is a text notification sent via Wtelegram.",
    )


if __name__ == "__main__":
    main()
