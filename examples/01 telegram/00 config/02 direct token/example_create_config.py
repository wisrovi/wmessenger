"""Example: Direct Token Configuration.

Demonstrates initializing Wtelegram by passing the bot API token directly.
"""

from wconnect import Wtelegram

# Configuration constants
TELEGRAM_TOKEN = "8823336064:AAE2sky0B4vOD5_z2cKsDekv4T9LSKiSlGA"
DEFAULT_CHAT_ID = "6586101740"


def main() -> None:
    """Demonstrate direct token bot initialization."""
    print("=== Direct Token Configuration ===")
    bot = Wtelegram(token=TELEGRAM_TOKEN)
    print(
        f"[SUCCESS] Bot initialized with token: {TELEGRAM_TOKEN[:10]}... (Running: {bot.is_running})"
    )
    print(f"  - Target Chat ID: {DEFAULT_CHAT_ID}")
    print("  - Ready to send/receive messages using direct token parameter.")


if __name__ == "__main__":
    main()
