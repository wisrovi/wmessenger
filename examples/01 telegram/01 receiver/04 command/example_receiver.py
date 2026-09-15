"""Example: Receiver for Bot Commands.

Demonstrates registering command handlers (/start, /status, /help).
"""

import os

from wconnect import WMessage, Wtelegram

if "TELEGRAM_BOT_TOKEN" not in os.environ:
    os.environ["TELEGRAM_BOT_TOKEN"] = "8823336064:AAE2sky0B4vOD5_z2cKsDekv4T9LSKiSlGA"

bot = Wtelegram()


@bot.on_command(command="start")
def handle_start(message: WMessage) -> None:
    """Handle /start command."""
    username = message.username or message.user_id
    print(f"[COMMAND /start] From {username}")
    bot.send(
        to=message.chat_id,
        message=f"Welcome {username}! Send /status or /help to interact.",
    )


@bot.on_command(command="status")
def handle_status(message: WMessage) -> None:
    """Handle /status command."""
    print(f"[COMMAND /status] From {message.username}")
    bot.send(
        to=message.chat_id,
        message="System status: All services operational ✅",
    )


@bot.on_command(command="help")
def handle_help(message: WMessage) -> None:
    """Handle /help command."""
    bot.send(
        to=message.chat_id,
        message="Available commands: /start, /status, /help",
    )


def main() -> None:
    """Start command receiver bot."""
    print("=== Bot Command Receiver ===")
    print("[STARTING] Listening for bot commands (/start, /status, /help)...")
    bot.run_consumers(block=True)


if __name__ == "__main__":
    main()
