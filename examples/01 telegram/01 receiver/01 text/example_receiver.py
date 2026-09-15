"""Example: Receiver for Text Messages.

Demonstrates listening to incoming text messages using Wtelegram.
"""

import os

from wconnect import WMessage, Wtelegram

# Fallback environment setting if TELEGRAM_BOT_TOKEN is not defined
if "TELEGRAM_BOT_TOKEN" not in os.environ:
    os.environ["TELEGRAM_BOT_TOKEN"] = "8823336064:AAE2sky0B4vOD5_z2cKsDekv4T9LSKiSlGA"

bot = Wtelegram()


@bot.on_message(value_type="text")
def handle_text_messages(message: WMessage) -> None:
    """Consumer for text messages."""
    username = message.username or message.user_id
    print(
        f"[TEXT RECEIVED] From {username} (Chat ID: {message.chat_id}): {message.text}"
    )
    bot.send(
        to=message.chat_id,
        message=f"Received your message: '{message.text}'",
    )


def main() -> None:
    """Start text receiver bot."""
    print("=== Text Message Receiver Bot ===")
    print("[STARTING] Listening for incoming text messages...")
    bot.run_consumers(block=True)


if __name__ == "__main__":
    main()
