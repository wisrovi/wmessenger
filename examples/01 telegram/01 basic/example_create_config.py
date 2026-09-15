"""Example: Professional Telegram Bot Configuration Installer Module.

Stores Telegram bot credentials, bot metadata, and authorized users into WAuth vault.
"""

from typing import Optional

from wauth import WAuth

# Configuration constants
DB_PATH = "./my_secrets.db"
DEFAULT_BOT_NAME = "Perseus_bot"
DEFAULT_BOT_USERNAME = "WPerseus_bot"
DEFAULT_TELEGRAM_TOKEN = "8823336064:AAE2sky0B4vOD5_z2cKsDekv4T9LSKiSlGA"
DEFAULT_AUTHORIZED_USERS = ["6586101740"]


def save_telegram_config(
    token: str = DEFAULT_TELEGRAM_TOKEN,
    authorized_users: Optional[list[str]] = None,
    bot_name: str = DEFAULT_BOT_NAME,
    bot_username: str = DEFAULT_BOT_USERNAME,
) -> bool:
    """Save Telegram bot credentials and authorized users into the WAuth vault.

    Args:
        token: Telegram bot API token.
        authorized_users: List of authorized user chat IDs.
        bot_name: Display name of the bot.
        bot_username: Username of the bot.

    Returns:
        bool: True if configuration was stored successfully.
    """
    if authorized_users is None:
        authorized_users = DEFAULT_AUTHORIZED_USERS

    vault = WAuth(db_path=DB_PATH)

    # Store credentials and metadata in the vault
    vault.set("telegram_token", token)
    vault.set("authorized_users", ",".join(authorized_users))
    vault.set("telegram_bot_name", bot_name)
    vault.set("telegram_bot_username", bot_username)

    masked_token = f"{token[:10]}..." if len(token) > 10 else "***"
    print(f"[SUCCESS] Credentials saved in vault: {DB_PATH}")
    print(f"  - Bot Name: {bot_name} (@{bot_username})")
    print(f"  - Token: {masked_token}")
    print(f"  - Authorized Users: {authorized_users}")
    return True


def main() -> None:
    """Execute the configuration initialization workflow."""
    print("=== Initializing Telegram Vault Configuration ===")
    save_telegram_config()


if __name__ == "__main__":
    main()
