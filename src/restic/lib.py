from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from utilities.os import temp_environ

from restic.settings import SETTINGS

if TYPE_CHECKING:
    from typed_settings import Secret
    from utilities.types import PathLike


def backup(
    path: PathLike,
    repo: str,
    /,
    *,
    password: Secret[str] | PathLike = SETTINGS.password,
) -> None:
    with temp_environ(RESTIC_PASSWORD=1):
        a


__all__ = ["backup"]
