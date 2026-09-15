"""Example: Receiver for Document Files.

Demonstrates receiving document files (CSVs, PDFs, ZIPs) with in-memory parsing and auto-saving.
"""

import os

from wconnect import WMessage, Wtelegram

if "TELEGRAM_BOT_TOKEN" not in os.environ:
    os.environ["TELEGRAM_BOT_TOKEN"] = "8823336064:AAE2sky0B4vOD5_z2cKsDekv4T9LSKiSlGA"

DOWNLOADS_DIR = "./downloads"

bot = Wtelegram(auto_save_in=DOWNLOADS_DIR)


@bot.on_message(value_type="document")
def handle_document_messages(message: WMessage) -> None:
    """Consumer for document files."""
    file_bytes = message.file.content
    print(
        f"[DOCUMENT RECEIVED] Name: {message.file.name}, Size: {len(file_bytes)} bytes"
    )
    print(f"[AUTO-SAVED] Location: {message.saved_path}")

    if message.file.name.endswith(".csv"):
        print("[CSV PARSER] Processing in-memory dataset...")

    bot.send(
        to=message.chat_id,
        message=f"📄 Document '{message.file.name}' saved to '{message.saved_path}'.",
    )


def main() -> None:
    """Start document receiver bot."""
    print("=== Document Receiver Bot ===")
    print("[STARTING] Listening for incoming document files...")
    bot.run_consumers(block=True)


if __name__ == "__main__":
    main()
