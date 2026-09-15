"""Example: Environment Variable Telegram Receiver.

Demonstrates initializing Wtelegram using the TELEGRAM_BOT_TOKEN environment variable.
"""

import os

from wconnect import WMessage, Wtelegram

# Fallback setting for environment variable in example script if not set
if "TELEGRAM_BOT_TOKEN" not in os.environ:
    os.environ["TELEGRAM_BOT_TOKEN"] = "8823336064:AAE2sky0B4vOD5_z2cKsDekv4T9LSKiSlGA"

DOWNLOADS_DIR = "./downloads"
AUTHORIZED_USERS = ["6586101740"]

bot = Wtelegram(auto_save_in=DOWNLOADS_DIR)


@bot.command(command="status")
def handle_status_command(message: WMessage) -> None:
    """Handle the /status command."""
    username = message.username or message.user_id
    print(f"[COMMAND /status] Received from {username}")
    bot.send(
        to=message.chat_id,
        message=f"Hello {username}, Environment Variable bot is online! ✅",
    )


@bot.consumer(value_type="text")
def handle_text_messages(message: WMessage) -> None:
    """Handle general text messages."""
    print(f"[TEXT MESSAGE] From {message.username}: {message.text}")


@bot.consumer(value_type="image")
def handle_image_messages(message: WMessage) -> None:
    """Handle incoming image attachments."""
    if AUTHORIZED_USERS and message.user_id not in AUTHORIZED_USERS:
        print(f"[UNAUTHORIZED IMAGE] Access denied for User ID: {message.user_id}")
        bot.send(
            to=message.chat_id,
            message="🚫 Access denied: You are not authorized.",
        )
        return

    print(f"[IMAGE RECEIVED] From {message.username} ({message.file.name})")
    print(f"[IMAGE AUTO-SAVED] Location: {message.saved_path}")
    bot.send(
        to=message.chat_id,
        message=f"📷 Image '{message.file.name}' saved to '{message.saved_path}'.",
    )


@bot.consumer(value_type="document")
def handle_document_messages(message: WMessage) -> None:
    """Handle incoming document files."""
    file_bytes = message.file.content
    print(
        f"[DOCUMENT RECEIVED] Name: {message.file.name}, Size: {len(file_bytes)} bytes"
    )
    print(f"[DOCUMENT AUTO-SAVED] Location: {message.saved_path}")

    bot.send(
        to=message.chat_id,
        message=f"📄 Document '{message.file.name}' saved to '{message.saved_path}'.",
    )


def main() -> None:
    """Execute environment variable receiver bot."""
    print("=== Initializing Environment Variable Telegram Receiver Bot ===")
    token_preview = os.environ.get("TELEGRAM_BOT_TOKEN", "")[:10]
    print(f"[ENV] TELEGRAM_BOT_TOKEN is set to: {token_preview}...")
    print("[STARTING] Listening for incoming messages...")
    bot.run_consumers(block=True)


if __name__ == "__main__":
    main()
