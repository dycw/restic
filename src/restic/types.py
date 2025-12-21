from __future__ import annotations

from typed_settings import Secret
from utilities.types import PathLike

type PasswordLike = Secret[str] | PathLike

__all__ = ["PasswordLike"]
