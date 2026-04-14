"""WFile: File handling for telegram messages."""

import os
from typing import Optional, Union


class WFile:
    """Represents a file attached to a telegram message."""

    def __init__(
        self,
        content: Optional[bytes] = None,
        name: Optional[str] = None,
        file_id: Optional[str] = None,
        file_path: Optional[str] = None,
        file_url: Optional[str] = None,
        file_size: Optional[int] = None,
        mime_type: Optional[str] = None,
    ):
        self._content = content
        self._name = name or "unknown"
        self._file_id = file_id
        self._file_path = file_path
        self._file_url = file_url
        self._file_size = file_size
        self._mime_type = mime_type

    @property
    def content(self) -> bytes:
        """Return the file bytes. Downloads if needed."""
        if self._content is not None:
            return self._content
        # If we have a file_path, read from disk
        if self._file_path and os.path.exists(self._file_path):
            with open(self._file_path, "rb") as f:
                self._content = f.read()
            return self._content
        return b""

    @property
    def name(self) -> str:
        return self._name

    @property
    def file_id(self) -> Optional[str]:
        return self._file_id

    @property
    def file_size(self) -> Optional[int]:
        return self._file_size or (len(self._content) if self._content else None)

    @property
    def mime_type(self) -> Optional[str]:
        return self._mime_type

    @property
    def url(self) -> Optional[str]:
        return self._file_url

    def save(self, path: str) -> str:
        """Save the file to the given path. Returns the final path."""
        # Ensure parent directory exists
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)

        data = self.content
        with open(path, "wb") as f:
            f.write(data)
        return path

    @classmethod
    def from_telegram_file(cls, tg_file) -> "WFile":
        """Create a WFile from a telegram-bot file object."""
        return cls(
            file_id=tg_file.file_id,
            name=tg_file.file_name or "unknown",
            file_size=tg_file.file_size,
            mime_type=getattr(tg_file, "mime_type", None),
        )

    def __repr__(self) -> str:
        return f"WFile(name='{self._name}', size={self.file_size})"
