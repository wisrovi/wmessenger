"""Example: Professional Telegram Bot Receiver Module.

Demonstrates receiving commands, text messages, images, and documents using Wtelegram and WAuth.
"""

import os

from wauth import WAuth

from wconnect import WMessage, Wtelegram

# Configuration constants
DB_PATH = "./my_secrets.db"
DOWNLOADS_DIR = "./downloads"


def get_authorized_users(vault: WAuth) -> list[str]:
    """Retrieve list of authorized user IDs from vault.

    Args:
        vault: Initialized WAuth instance.

    Returns:
        list[str]: List of user ID strings authorized to interact with protected endpoints.
    """
    authorized_raw = vault.get("authorized_users") or ""
    return [user_id.strip() for user_id in authorized_raw.split(",") if user_id.strip()]


def setup_bot_handlers(bot: Wtelegram, authorized_users: list[str]) -> None:
    """Register command and consumer message handlers on the Wtelegram bot instance.

    Args:
        bot: Initialized Wtelegram bot instance.
        authorized_users: List of authorized user IDs for access control.
    """

    # 1. Command handler: /status
    @bot.command(command="status")
    def handle_status_command(message: WMessage) -> None:
        """Handle the /status command and reply with system status."""
        username = message.username or message.user_id
        print(
            f"[COMMAND /status] Received from {username} (Chat ID: {message.chat_id})"
        )
        bot.send(
            to=message.chat_id,
            message=f"Hello {username}, the Telegram Bot service is online and operational! ✅",
        )

    # 2. Text message consumer
    @bot.consumer(value_type="text")
    def handle_text_messages(message: WMessage) -> None:
        """Handle incoming general text messages."""
        print(f"[TEXT MESSAGE] From {message.username}: {message.text}")

    # 3. Image message consumer
    @bot.consumer(value_type="image")
    def handle_image_messages(message: WMessage) -> None:
        """Handle incoming image attachments and save them locally."""
        if authorized_users and message.user_id not in authorized_users:
            print(f"[UNAUTHORIZED IMAGE] Access denied for User ID: {message.user_id}")
            bot.send(
                to=message.chat_id,
                message="🚫 Access denied: You are not authorized to upload images.",
            )
            return

        print(f"[IMAGE RECEIVED] From {message.username} ({message.file.name})")
        os.makedirs(DOWNLOADS_DIR, exist_ok=True)
        saved_path = message.file.save(os.path.join(DOWNLOADS_DIR, message.file.name))
        print(f"[IMAGE SAVED] Location: {saved_path}")
        bot.send(
            to=message.chat_id,
            message=f"📷 Image '{message.file.name}' received and saved successfully.",
        )

    # 4. Document message consumer
    @bot.consumer(value_type="document")
    def handle_document_messages(message: WMessage) -> None:
        """Handle incoming document files (CSVs, PDFs, ZIPs) with in-memory inspection."""
        file_bytes = message.file.content
        print(
            f"[DOCUMENT RECEIVED] Name: {message.file.name}, Size: {len(file_bytes)} bytes"
        )

        if message.file.name.endswith(".csv"):
            print("[CSV PROCESSING] Parsing in-memory CSV dataset...")

        bot.send(
            to=message.chat_id,
            message=f"📄 Document '{message.file.name}' ({len(file_bytes)} bytes) processed.",
        )


def main() -> None:
    """Initialize WAuth vault, set up Wtelegram bot, and start polling."""
    print("=== Initializing Telegram Receiver Bot ===")
    if not os.path.exists(DB_PATH):
        print(
            f"[ERROR] Vault database '{DB_PATH}' not found. Please run example_create_config.py first."
        )
        return

    vault = WAuth(db_path=DB_PATH)
    authorized_users = get_authorized_users(vault)
    print(f"[CONFIG] Loaded {len(authorized_users)} authorized user(s) from vault.")

    bot = Wtelegram(auth_instance=vault)
    setup_bot_handlers(bot=bot, authorized_users=authorized_users)

    print("[STARTING] Bot is now listening for incoming messages...")
    bot.run_bot()


if __name__ == "__main__":
    main()
