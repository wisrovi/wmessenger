"""Wtelegram: Telegram bot wrapper with decorators for commands and message handlers."""

import asyncio
import inspect
import os
import threading
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Union

import requests
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from .wfile import WFile
from .wmessage import WMessage


class Wtelegram:
    """Telegram bot wrapper with simple decorators for commands and messages."""

    def __init__(self, token: Optional[str] = None, auth_instance: Optional[Any] = None):
        """
        Initialize Wtelegram.

        Args:
            token: Telegram bot token directly. If not provided, tries to get from auth_instance.
            auth_instance: A WAuth instance or any object with token storage.
        """
        self._token = token
        self._auth_instance = auth_instance

        # Try to get token from auth_instance
        if self._token is None and self._auth_instance is not None:
            self._token = self._resolve_token()

        if self._token is None:
            # Try environment variable
            self._token = os.environ.get("TELEGRAM_BOT_TOKEN", "")

        self._application: Optional[Application] = None
        self._command_handlers: Dict[str, Callable] = {}
        self._message_handlers: List[dict] = []
        self._running = False

    def _resolve_token(self) -> Optional[str]:
        """Try to resolve bot token from auth_instance."""
        if self._auth_instance is None:
            return None

        # Try common attribute names on the auth instance
        for attr in ("telegram_token", "bot_token", "token", "tg_token"):
            val = getattr(self._auth_instance, attr, None)
            if val and isinstance(val, str) and val.strip():
                return val

        # If auth_instance has a get/get_value method
        if hasattr(self._auth_instance, "get"):
            for key in ("telegram_token", "bot_token", "token", "tg_token"):
                try:
                    val = self._auth_instance.get(key)
                    if val:
                        return val
                except Exception:
                    pass

        # If auth_instance has a read/get_db method
        if hasattr(self._auth_instance, "read"):
            for key in ("telegram_token", "bot_token", "token", "tg_token"):
                try:
                    val = self._auth_instance.read(key)
                    if val:
                        return val
                except Exception:
                    pass

        return None

    def _get_application(self) -> Application:
        """Get or create the telegram Application."""
        if self._application is None:
            self._application = Application.builder().token(self._token).build()
        return self._application

    # ----------------------------------------------------------------
    # Decorators
    # ----------------------------------------------------------------

    def command(self, command: str = "start"):
        """Decorator to register a command handler.

        Usage:
            @tg.command(command="status")
            def get_status(message: WMessage):
                ...
        """

        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
                wmsg = WMessage.from_telegram_update(update, context.bot)
                # Only handle if it's actually this command
                if wmsg.is_command and wmsg.command == command:
                    if inspect.iscoroutinefunction(func):
                        await func(wmsg)
                    else:
                        # Run sync function in thread to not block
                        loop = asyncio.get_event_loop()
                        await loop.run_in_executor(None, func, wmsg)

            self._command_handlers[command] = wrapper
            return wrapper

        return decorator

    def consumer(
        self,
        value_type: str = "text",
        from_user: Optional[str] = None,
    ):
        """Decorator to register a message consumer.

        Args:
            value_type: "text", "image", "document", "all"
            from_user: If set, only handle messages from this user_id

        Usage:
            @tg.consumer(value_type="text")
            def handle_text(message: WMessage):
                ...

            @tg.consumer(value_type="image", from_user="12345678")
            def handle_my_images(message: WMessage):
                ...
        """

        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
                wmsg = WMessage.from_telegram_update(update, context.bot)

                # Check from_user filter
                if from_user is not None:
                    if wmsg.user_id != from_user:
                        return

                # Check value type filter
                if value_type == "all":
                    pass  # accept everything
                elif value_type == "text":
                    if wmsg.value_type != "text":
                        return
                elif value_type == "image":
                    if wmsg.value_type not in ("image",):
                        return
                elif value_type == "document":
                    if wmsg.value_type not in ("document",):
                        return

                if inspect.iscoroutinefunction(func):
                    await func(wmsg)
                else:
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(None, func, wmsg)

            self._message_handlers.append(
                {"func": wrapper, "value_type": value_type, "from_user": from_user}
            )
            return wrapper

        return decorator

    # ----------------------------------------------------------------
    # Sending methods
    # ----------------------------------------------------------------

    def send(self, to: Union[int, str], message: str, **kwargs) -> bool:
        """Send a text message to a chat/user.

        Args:
            to: Chat ID or user ID
            message: Text message to send

        Returns:
            True if sent successfully
        """
        url = f"https://api.telegram.org/bot{self._token}/sendMessage"
        data = {"chat_id": to, "text": message}
        data.update(kwargs)
        resp = requests.post(url, json=data, timeout=30)
        return resp.status_code == 200

    def send_photo(self, to: Union[int, str], photo: Any, caption: Optional[str] = None) -> bool:
        """Send a photo to a chat/user.

        Args:
            to: Chat ID or user ID
            photo: File path, URL, or file-like object
            caption: Optional caption
        """
        url = f"https://api.telegram.org/bot{self._token}/sendPhoto"
        data: Dict[str, Any] = {"chat_id": to}
        if caption:
            data["caption"] = caption

        # Determine if photo is a URL or file
        if isinstance(photo, str) and photo.startswith("http"):
            data["photo"] = photo
            resp = requests.post(url, json=data, timeout=30)
        else:
            # It's a file path
            with open(photo, "rb") as f:
                files = {"photo": f}
                resp = requests.post(url, data=data, files=files, timeout=30)

        return resp.status_code == 200

    def send_image(
        self,
        to: Union[int, str],
        path: Optional[str] = None,
        url: Optional[str] = None,
        caption: Optional[str] = None,
    ) -> bool:
        """Send an image to a chat/user.

        Args:
            to: Chat ID or user ID
            path: Local file path
            url: Image URL
            caption: Optional caption
        """
        if url:
            return self.send_photo(to, url, caption)
        elif path:
            return self.send_photo(to, path, caption)
        else:
            raise ValueError("Either 'path' or 'url' must be provided")

    def send_document(
        self,
        to: Union[int, str],
        path: Optional[str] = None,
        file: Optional[WFile] = None,
        caption: Optional[str] = None,
    ) -> bool:
        """Send a document to a chat/user.

        Args:
            to: Chat ID or user ID
            path: Local file path
            file: WFile object with content
            caption: Optional caption
        """
        url = f"https://api.telegram.org/bot{self._token}/sendDocument"
        data: Dict[str, Any] = {"chat_id": to}
        if caption:
            data["caption"] = caption

        if file is not None:
            # Send from WFile object
            with requests.post(url, data=data, timeout=30) as resp_init:
                pass
            files = {"document": (file.name, file.content)}
            resp = requests.post(url, data=data, files=files, timeout=30)
        elif path:
            filename = os.path.basename(path)
            with open(path, "rb") as f:
                files = {"document": (filename, f)}
                resp = requests.post(url, data=data, files=files, timeout=30)
        else:
            raise ValueError("Either 'path' or 'file' must be provided")

        return resp.status_code == 200

    # ----------------------------------------------------------------
    # Bot lifecycle
    # ----------------------------------------------------------------

    def _setup_handlers(self):
        """Register all handlers with the application."""
        app = self._get_application()

        # Register command handlers
        for cmd, handler in self._command_handlers.items():
            app.add_handler(CommandHandler(cmd, handler))

        # Register message handlers
        for handler_info in self._message_handlers:
            value_type = handler_info["value_type"]
            handler_func = handler_info["func"]

            if value_type == "text":
                app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler_func))
            elif value_type == "image":
                app.add_handler(
                    MessageHandler(
                        filters.PHOTO | filters.Document.ALL,
                        handler_func,
                    )
                )
            elif value_type == "document":
                app.add_handler(MessageHandler(filters.Document.ALL, handler_func))
            else:
                app.add_handler(MessageHandler(filters.ALL, handler_func))

    def run_bot(self, polling: bool = True):
        """Start the telegram bot.

        Args:
            polling: If True, use polling (default). If False, use webhook.
        """
        self._setup_handlers()
        app = self._get_application()

        if polling:
            app.run_polling()
        else:
            app.run_webhook()

    def run_async(self, polling: bool = True):
        """Run the bot in a background thread (non-blocking)."""

        def _run():
            self._setup_handlers()
            app = self._get_application()
            if polling:
                app.run_polling()
            else:
                app.run_webhook()

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        self._running = True
        return thread

    def stop_bot(self):
        """Stop the running bot."""
        if self._application and self._running:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._application.stop())
            self._running = False

    @property
    def is_running(self) -> bool:
        return self._running
