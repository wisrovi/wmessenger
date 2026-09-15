"""Example: Image Report Sender.

Demonstrates sending images from local file paths or public URLs.
"""

import os
from typing import Optional, Union

from wconnect import Wtelegram

if "TELEGRAM_BOT_TOKEN" not in os.environ:
    os.environ["TELEGRAM_BOT_TOKEN"] = "8823336064:AAE2sky0B4vOD5_z2cKsDekv4T9LSKiSlGA"

DEFAULT_CHAT_ID = "6586101740"


def send_image_report(
    chat_id: Union[int, str],
    image: str,
    caption: Optional[str] = None,
) -> bool:
    """Send an image report automatically detecting whether 'image' is a URL or local file path."""
    with Wtelegram() as producer:
        if image.startswith(("http://", "https://")):
            success = producer.send_image(to=chat_id, url=image, caption=caption)
        elif os.path.exists(image):
            success = producer.send_image(to=chat_id, path=image, caption=caption)
        else:
            print(f"[WARNING] Image path '{image}' does not exist locally.")
            return False

        if success:
            print(f"[SUCCESS] Image sent to {chat_id}")
        else:
            print(f"[ERROR] Failed to send image to {chat_id}")
        return success


def main() -> None:
    """Execute image sender workflow."""
    print("=== Image Report Sender ===")
    send_image_report(
        chat_id=DEFAULT_CHAT_ID,
        image="https://httpbin.org/image/png",
        caption="Sample analytics chart",
    )


if __name__ == "__main__":
    main()
