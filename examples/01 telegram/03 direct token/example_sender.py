"""Example: Direct Token Telegram Sender.

Demonstrates initializing Wtelegram by passing the bot token directly.
"""

import os
from typing import Optional, Union

from wconnect import WFile, Wtelegram

# Configuration constants
TELEGRAM_TOKEN = "8823336064:AAE2sky0B4vOD5_z2cKsDekv4T9LSKiSlGA"
DEFAULT_CHAT_ID = "6586101740"


def send_text_notification(
    chat_id: Union[int, str],
    message: str,
) -> bool:
    """Send a text notification directly using token."""
    with Wtelegram(token=TELEGRAM_TOKEN) as producer:
        success = producer.send(to=chat_id, message=message)
        if success:
            print(f"[SUCCESS] Text message delivered to {chat_id}")
        else:
            print(f"[ERROR] Failed to deliver text message to {chat_id}")
        return success


def send_image_report(
    chat_id: Union[int, str],
    image: str,
    caption: Optional[str] = None,
) -> bool:
    """Send an image report directly using token."""
    with Wtelegram(token=TELEGRAM_TOKEN) as producer:
        if image.startswith(("http://", "https://")):
            success = producer.send_image(to=chat_id, url=image, caption=caption)
        elif os.path.exists(image):
            success = producer.send_image(to=chat_id, path=image, caption=caption)
        else:
            print(f"[WARNING] Image path '{image}' does not exist locally.")
            return False

        if success:
            print(f"[SUCCESS] Image sent to {chat_id}")
        else:
            print(f"[ERROR] Failed to send image to {chat_id}")
        return success


def send_document_file(
    chat_id: Union[int, str],
    file: Union[str, WFile],
    caption: Optional[str] = None,
) -> bool:
    """Send a document file directly using token."""
    with Wtelegram(token=TELEGRAM_TOKEN) as producer:
        if isinstance(file, WFile):
            success = producer.send_document(to=chat_id, file=file, caption=caption)
        elif isinstance(file, str) and os.path.exists(file):
            success = producer.send_document(to=chat_id, path=file, caption=caption)
        else:
            print(f"[WARNING] Document file '{file}' does not exist.")
            return False

        if success:
            print(f"[SUCCESS] Document sent to {chat_id}")
        else:
            print(f"[ERROR] Failed to send document to {chat_id}")
        return success


def main() -> None:
    """Execute direct token sender workflow."""
    print("=== Direct Token Sender ===")
    send_text_notification(
        chat_id=DEFAULT_CHAT_ID,
        message="✅ Notification sent via direct token initialization.",
    )

    send_image_report(
        chat_id=DEFAULT_CHAT_ID,
        image="https://httpbin.org/image/png",
        caption="Sample analytics chart (Direct Token)",
    )

    report_data = b"timestamp,status\n2026-09-15,SUCCESS"
    csv_file = WFile(content=report_data, name="direct_summary.csv")
    send_document_file(
        chat_id=DEFAULT_CHAT_ID,
        file=csv_file,
        caption="📊 Summary export (Direct Token)",
    )


if __name__ == "__main__":
    main()
