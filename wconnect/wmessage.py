"""WMessage: Wrapper for incoming telegram messages."""

import os
from typing import Optional

from .wfile import WFile


class WMessage:
    """Wraps a telegram message with convenient properties."""

    def __init__(
        self,
        chat_id: int,
        user_id: int,
        text: Optional[str] = None,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        file: Optional[WFile] = None,
        value_type: str = "text",
        message_id: Optional[int] = None,
        is_command: bool = False,
        command: Optional[str] = None,
        saved_path: Optional[str] = None,
    ):
        self._chat_id = chat_id
        self._user_id = user_id
        self._text = text or ""
        self._username = username
        self._first_name = first_name
        self._last_name = last_name
        self._file = file
        self._value_type = value_type
        self._message_id = message_id
        self._is_command = is_command
        self._command = command
        self._saved_path = saved_path

    @property
    def chat_id(self) -> int:
        return self._chat_id

    @property
    def user_id(self) -> str:
        return str(self._user_id)

    @property
    def text(self) -> str:
        return self._text

    @property
    def username(self) -> Optional[str]:
        if self._username:
            return self._username
        if self._first_name:
            return self._first_name
        return str(self._user_id)

    @property
    def file(self) -> WFile:
        if self._file is None:
            self._file = WFile()
        return self._file

    @property
    def value_type(self) -> str:
        return self._value_type

    @property
    def message_id(self) -> Optional[int]:
        return self._message_id

    @property
    def is_command(self) -> bool:
        return self._is_command

    @property
    def command(self) -> Optional[str]:
        return self._command

    @property
    def saved_path(self) -> Optional[str]:
        return self._saved_path

    @saved_path.setter
    def saved_path(self, value: Optional[str]) -> None:
        self._saved_path = value

    @classmethod
    def from_telegram_update(
        cls, update, bot=None, auto_save_in: Optional[str] = None
    ) -> "WMessage":
        """Create a WMessage from a telegram Update object."""
        msg = update.effective_message
        user = update.effective_user

        chat_id = msg.chat_id
        user_id = user.id if user else 0
        username = user.username if user else None
        first_name = user.first_name if user else None
        last_name = user.last_name if user else None
        text = msg.text or msg.caption or ""
        message_id = msg.message_id
        bot_token = bot.token if bot else None

        # Detect value type and build file
        value_type = "text"
        file = None

        if msg.photo:
            value_type = "image"
            photo = msg.photo[-1]  # highest resolution
            file = WFile(
                file_id=photo.file_id,
                name=f"photo_{message_id}.jpg",
                file_size=photo.file_size,
                mime_type="image/jpeg",
                bot_token=bot_token,
            )
        elif msg.document:
            value_type = "document"
            doc = msg.document
            file = WFile(
                file_id=doc.file_id,
                name=doc.file_name or "document",
                file_size=doc.file_size,
                mime_type=doc.mime_type,
                bot_token=bot_token,
            )
        elif msg.video:
            value_type = "image"
            video = msg.video
            file = WFile(
                file_id=video.file_id,
                name=f"video_{message_id}.mp4",
                file_size=video.file_size,
                mime_type=video.mime_type,
                bot_token=bot_token,
            )
        elif msg.audio:
            value_type = "document"
            audio = msg.audio
            file = WFile(
                file_id=audio.file_id,
                name=audio.file_name or audio.title or "audio",
                file_size=audio.file_size,
                mime_type=audio.mime_type,
                bot_token=bot_token,
            )
        elif msg.voice:
            value_type = "document"
            voice = msg.voice
            file = WFile(
                file_id=voice.file_id,
                name=f"voice_{message_id}.ogg",
                file_size=voice.file_size,
                mime_type="audio/ogg",
                bot_token=bot_token,
            )

        # Handle auto-saving if auto_save_in path is provided
        saved_path = None
        if auto_save_in and file and file.file_id:
            os.makedirs(auto_save_in, exist_ok=True)
            target_path = os.path.join(auto_save_in, file.name)
            saved_path = file.save(target_path)

        # Detect commands
        is_command = False
        command = None
        if text.startswith("/"):
            parts = text.split()
            command = parts[0][1:].split("@")[0]  # strip bot mention
            is_command = True

        return cls(
            chat_id=chat_id,
            user_id=user_id,
            text=text,
            username=username,
            first_name=first_name,
            last_name=last_name,
            file=file,
            value_type=value_type,
            message_id=message_id,
            is_command=is_command,
            command=command,
            saved_path=saved_path,
        )

    def __repr__(self) -> str:
        return f"WMessage(from={self.username}, type={self.value_type})"
