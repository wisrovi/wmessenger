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
    producer: Wtelegram,
    chat_id: Union[int, str],
    message: str,
) -> bool:
    """Send a text notification to a Telegram user/chat.

    Args:
        producer: Initialized Wtelegram bot instance.
        chat_id: Target user or chat ID.
        message: Content of the text message to send.

    Returns:
        bool: True if the message was delivered successfully, False otherwise.
    """
    success = producer.send(to=chat_id, message=message)
    if success:
        print(f"[SUCCESS] Text message delivered to {chat_id}")
    else:
        print(f"[ERROR] Failed to deliver text message to {chat_id}")
    return success


def send_image_report(
    producer: Wtelegram,
    chat_id: Union[int, str],
    image_path: Optional[str] = None,
    image_url: Optional[str] = None,
    caption: Optional[str] = None,
) -> bool:
    """Send an image report from a local file path or public URL.

    Args:
        producer: Initialized Wtelegram bot instance.
        chat_id: Target user or chat ID.
        image_path: Optional local path to an image file.
        image_url: Optional public URL of an image.
        caption: Optional descriptive caption for the image.

    Returns:
        bool: True if the image was sent successfully, False otherwise.
    """
    if image_path and os.path.exists(image_path):
        success = producer.send_image(to=chat_id, path=image_path, caption=caption)
    elif image_url:
        success = producer.send_image(to=chat_id, url=image_url, caption=caption)
    else:
        print(
            "[WARNING] Neither a valid local image_path nor an image_url was provided."
        )
        return False

    if success:
        print(f"[SUCCESS] Image sent to {chat_id}")
    else:
        print(f"[ERROR] Failed to send image to {chat_id}")
    return success


def send_document_file(
    producer: Wtelegram,
    chat_id: Union[int, str],
    file_path: Optional[str] = None,
    wfile: Optional[WFile] = None,
    caption: Optional[str] = None,
) -> bool:
    """Send a document file (local path or WFile in-memory object).

    Args:
        producer: Initialized Wtelegram bot instance.
        chat_id: Target user or chat ID.
        file_path: Optional local path to a document file.
        wfile: Optional WFile in-memory file instance.
        caption: Optional descriptive caption for the document.

    Returns:
        bool: True if the document was sent successfully, False otherwise.
    """
    if wfile is not None:
        success = producer.send_document(to=chat_id, file=wfile, caption=caption)
    elif file_path and os.path.exists(file_path):
        success = producer.send_document(to=chat_id, path=file_path, caption=caption)
    else:
        print(
            "[WARNING] Neither a valid local file_path nor a WFile object was provided."
        )
        return False

    if success:
        print(f"[SUCCESS] Document sent to {chat_id}")
    else:
        print(f"[ERROR] Failed to send document to {chat_id}")
    return success


def main() -> None:
    """Execute the professional sender workflow."""
    vault = WAuth(db_path=DB_PATH)

    with Wtelegram(auth_instance=vault) as producer:
        print("=== Sending Text Message ===")
        send_text_notification(
            producer=producer,
            chat_id=DEFAULT_CHAT_ID,
            message="✅ Operation completed successfully.",
        )

        print("\n=== Sending Image ===")
        send_image_report(
            producer=producer,
            chat_id=DEFAULT_CHAT_ID,
            image_url="https://httpbin.org/image/png",
            caption="Sample analytics chart",
        )

        print("\n=== Sending Document ===")
        report_data = b"timestamp,status,count\n2026-09-15,OK,100"
        csv_file = WFile(content=report_data, name="daily_summary.csv")
        send_document_file(
            producer=producer,
            chat_id=DEFAULT_CHAT_ID,
            wfile=csv_file,
            caption="📊 Daily summary export",
        )


if __name__ == "__main__":
    main()
