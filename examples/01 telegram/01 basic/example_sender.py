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
    db_path: str = DB_PATH,
) -> bool:
    """Send a text notification to a Telegram user/chat using vault credentials.

    Args:
        chat_id: Target user or chat ID.
        message: Content of the text message to send.
        db_path: Path to the WAuth vault database.

    Returns:
        bool: True if the message was delivered successfully, False otherwise.
    """
    vault = WAuth(db_path=db_path)
    with Wtelegram(auth_instance=vault) as producer:
        success = producer.send(to=chat_id, message=message)
        if success:
            print(f"[SUCCESS] Text message delivered to {chat_id}")
        else:
            print(f"[ERROR] Failed to deliver text message to {chat_id}")
        return success


def send_image_report(
    chat_id: Union[int, str],
    image_path: Optional[str] = None,
    image_url: Optional[str] = None,
    caption: Optional[str] = None,
    db_path: str = DB_PATH,
) -> bool:
    """Send an image report from a local file path or public URL using vault credentials.

    Args:
        chat_id: Target user or chat ID.
        image_path: Optional local path to an image file.
        image_url: Optional public URL of an image.
        caption: Optional descriptive caption for the image.
        db_path: Path to the WAuth vault database.

    Returns:
        bool: True if the image was sent successfully, False otherwise.
    """
    vault = WAuth(db_path=db_path)
    with Wtelegram(auth_instance=vault) as producer:
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
    chat_id: Union[int, str],
    file_path: Optional[str] = None,
    wfile: Optional[WFile] = None,
    caption: Optional[str] = None,
    db_path: str = DB_PATH,
) -> bool:
    """Send a document file (local path or WFile in-memory object) using vault credentials.

    Args:
        chat_id: Target user or chat ID.
        file_path: Optional local path to a document file.
        wfile: Optional WFile in-memory file instance.
        caption: Optional descriptive caption for the document.
        db_path: Path to the WAuth vault database.

    Returns:
        bool: True if the document was sent successfully, False otherwise.
    """
    vault = WAuth(db_path=db_path)
    with Wtelegram(auth_instance=vault) as producer:
        if wfile is not None:
            success = producer.send_document(to=chat_id, file=wfile, caption=caption)
        elif file_path and os.path.exists(file_path):
            success = producer.send_document(
                to=chat_id, path=file_path, caption=caption
            )
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
    print("=== Sending Text Message ===")
    send_text_notification(
        chat_id=DEFAULT_CHAT_ID,
        message="✅ Operation completed successfully.",
    )

    print("\n=== Sending Image ===")
    send_image_report(
        chat_id=DEFAULT_CHAT_ID,
        image_url="https://httpbin.org/image/png",
        caption="Sample analytics chart",
    )

    print("\n=== Sending Document ===")
    report_data = b"timestamp,status,count\n2026-09-15,OK,100"
    csv_file = WFile(content=report_data, name="daily_summary.csv")
    send_document_file(
        chat_id=DEFAULT_CHAT_ID,
        wfile=csv_file,
        caption="📊 Daily summary export",
    )


if __name__ == "__main__":
    main()
