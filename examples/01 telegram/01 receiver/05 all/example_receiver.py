"""Example: Catch-All Receiver.

Demonstrates receiving all message types (text, photos, documents, etc.) using value_type='all'.
"""

import os

from wconnect import WMessage, Wtelegram

if "TELEGRAM_BOT_TOKEN" not in os.environ:
    os.environ["TELEGRAM_BOT_TOKEN"] = "8823336064:AAE2sky0B4vOD5_z2cKsDekv4T9LSKiSlGA"

DOWNLOADS_DIR = "./downloads"

bot = Wtelegram(auto_save_in=DOWNLOADS_DIR)


@bot.on_message(value_type="all")
def handle_all_messages(message: WMessage) -> None:
    """Consumer for all message types."""
    print(
        f"[CATCH-ALL] Type: {message.value_type}, From: {message.username}, Text/Caption: '{message.text}'"
    )
    if message.saved_path:
        print(f"[ATTACHMENT SAVED] Location: {message.saved_path}")

    bot.send(
        to=message.chat_id,
        message=f"Received {message.value_type} message successfully.",
    )


def main() -> None:
    """Start catch-all receiver bot."""
    print("=== Catch-All Receiver Bot ===")
    print("[STARTING] Listening for all incoming message types...")
    bot.run_consumers(block=True)


if __name__ == "__main__":
    main()
