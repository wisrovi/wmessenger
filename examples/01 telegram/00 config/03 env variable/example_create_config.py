"""Example: Environment Variable Configuration.

Demonstrates initializing Wtelegram using TELEGRAM_BOT_TOKEN environment variable.
"""

import os

from wconnect import Wtelegram

# Set TELEGRAM_BOT_TOKEN in environment if not already set
if "TELEGRAM_BOT_TOKEN" not in os.environ:
    os.environ["TELEGRAM_BOT_TOKEN"] = "8823336064:AAE2sky0B4vOD5_z2cKsDekv4T9LSKiSlGA"

DEFAULT_CHAT_ID = "6586101740"


def main() -> None:
    """Demonstrate environment variable bot initialization."""
    print("=== Environment Variable Configuration ===")
    token_val = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    print(f"[ENV] TELEGRAM_BOT_TOKEN detected: {token_val[:10]}...")

    # Initializes automatically reading from TELEGRAM_BOT_TOKEN
    bot = Wtelegram()
    print(
        f"[SUCCESS] Bot initialized from environment variable. (Running: {bot.is_running})"
    )
    print("  - Ready to send/receive messages using TELEGRAM_BOT_TOKEN.")


if __name__ == "__main__":
    main()
