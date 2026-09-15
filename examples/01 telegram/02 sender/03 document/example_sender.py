"""Example: Document File Sender.

Demonstrates sending document files (local paths or WFile in-memory objects).
"""

import os
from typing import Optional, Union

from wconnect import WFile, Wtelegram

if "TELEGRAM_BOT_TOKEN" not in os.environ:
    os.environ["TELEGRAM_BOT_TOKEN"] = "8823336064:AAE2sky0B4vOD5_z2cKsDekv4T9LSKiSlGA"

DEFAULT_CHAT_ID = "6586101740"


def send_document_file(
    chat_id: Union[int, str],
    file: Union[str, WFile],
    caption: Optional[str] = None,
) -> bool:
    """Send a document file automatically handling local file path or WFile in-memory object."""
    with Wtelegram() as producer:
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
    """Execute document sender workflow."""
    print("=== Document File Sender ===")
    report_data = b"timestamp,status,count\n2026-09-15,OK,100"
    csv_file = WFile(content=report_data, name="daily_summary.csv")

    send_document_file(
        chat_id=DEFAULT_CHAT_ID,
        file=csv_file,
        caption="📊 Daily summary export",
    )


if __name__ == "__main__":
    main()
