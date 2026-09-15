"""Example: Receiver for Image Attachments.

Demonstrates receiving image attachments with auto-saving and user authorization.
"""

import os

from wconnect import WMessage, Wtelegram

if "TELEGRAM_BOT_TOKEN" not in os.environ:
    os.environ["TELEGRAM_BOT_TOKEN"] = "8823336064:AAE2sky0B4vOD5_z2cKsDekv4T9LSKiSlGA"

DOWNLOADS_DIR = "./downloads"
AUTHORIZED_USERS = ["6586101740"]

bot = Wtelegram(auto_save_in=DOWNLOADS_DIR)


@bot.on_message(value_type="image")
def handle_image_messages(message: WMessage) -> None:
    """Consumer for image attachments."""
    if AUTHORIZED_USERS and message.user_id not in AUTHORIZED_USERS:
        print(f"[UNAUTHORIZED] Image upload blocked for User ID: {message.user_id}")
        bot.send(to=message.chat_id, message="🚫 Access denied.")
        return

    print(f"[IMAGE RECEIVED] From {message.username} ({message.file.name})")
    print(f"[AUTO-SAVED] Location: {message.saved_path}")
    bot.send(
        to=message.chat_id,
        message=f"📷 Image saved successfully to '{message.saved_path}'.",
    )


def main() -> None:
    """Start image receiver bot."""
    print("=== Image Receiver Bot ===")
    print(f"[CONFIG] Auto saving images to '{DOWNLOADS_DIR}'")
    print("[STARTING] Listening for incoming images...")
    bot.run_consumers(block=True)


if __name__ == "__main__":
    main()
