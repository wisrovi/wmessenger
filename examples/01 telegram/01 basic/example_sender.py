"""Example: Professional Telegram Sender Module.

Demonstrates sending text, image, and document messages using Wtelegram and WAuth vault credentials.
"""

import os
from typing import Optional, Union

from wauth import WAuth

from wconnect import WFile, Wtelegram

# Configuration constants
DB_PATH = "./my_secrets.db"
DEFAULT_CHAT_ID = "6586101740"


def send_text_notification(
    chat_id: Union[int, str],
    message: str,
) -> bool:
    """Send a text notification to a Telegram user/chat using vault credentials.

    Args:
        chat_id: Target user or chat ID.
        message: Content of the text message to send.

    Returns:
        bool: True if the message was delivered successfully, False otherwise.
    """
    vault = WAuth(db_path=DB_PATH)
    with Wtelegram(auth_instance=vault) as producer:
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
    """Send an image report automatically detecting whether 'image' is a URL or local file path.

    Args:
        chat_id: Target user or chat ID.
        image: Local file path or public image URL.
        caption: Optional descriptive caption for the image.

    Returns:
        bool: True if the image was sent successfully, False otherwise.
    """
    vault = WAuth(db_path=DB_PATH)
    with Wtelegram(auth_instance=vault) as producer:
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
    """Send a document file automatically handling local file path or WFile in-memory object.

    Args:
        chat_id: Target user or chat ID.
        file: Local file path or WFile object.
        caption: Optional descriptive caption for the document.

    Returns:
        bool: True if the document was sent successfully, False otherwise.
    """
    vault = WAuth(db_path=DB_PATH)
    with Wtelegram(auth_instance=vault) as producer:
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
    """Execute the professional sender workflow."""
    print("=== Sending Text Message ===")
    send_text_notification(
        chat_id=DEFAULT_CHAT_ID,
        message="✅ Operation completed successfully.",
    )

    print("\n=== Sending Image ===")
    send_image_report(
        chat_id=DEFAULT_CHAT_ID,
        image="https://httpbin.org/image/png",
        caption="Sample analytics chart",
    )

    print("\n=== Sending Document ===")
    report_data = b"timestamp,status,count\n2026-09-15,OK,100"
    csv_file = WFile(content=report_data, name="daily_summary.csv")
    send_document_file(
        chat_id=DEFAULT_CHAT_ID,
        file=csv_file,
        caption="📊 Daily summary export",
    )


if __name__ == "__main__":
    main()
