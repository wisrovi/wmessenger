"""Example: Direct Token Telegram Receiver.

Demonstrates initializing Wtelegram by passing the bot token directly.
"""

from wconnect import WMessage, Wtelegram

# Configuration constants
TELEGRAM_TOKEN = "8823336064:AAE2sky0B4vOD5_z2cKsDekv4T9LSKiSlGA"
DOWNLOADS_DIR = "./downloads"
AUTHORIZED_USERS = ["6586101740"]

bot = Wtelegram(token=TELEGRAM_TOKEN, auto_save_in=DOWNLOADS_DIR)


@bot.command(command="status")
def handle_status_command(message: WMessage) -> None:
    """Handle the /status command."""
    username = message.username or message.user_id
    print(f"[COMMAND /status] Received from {username}")
    bot.send(
        to=message.chat_id,
        message=f"Hello {username}, Direct Token bot is online! ✅",
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
    """Execute direct token receiver bot."""
    print("=== Initializing Direct Token Telegram Receiver Bot ===")
    print("[STARTING] Listening for incoming messages...")
    bot.run_consumers(block=True)


if __name__ == "__main__":
    main()
