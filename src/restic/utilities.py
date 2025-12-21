from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING

from typed_settings import Secret
from utilities.os import temp_environ

from restic.settings import SETTINGS

if TYPE_CHECKING:
    from collections.abc import Iterator

    from restic.types import PasswordLike


@contextmanager
def yield_restic_password(
    *, password: PasswordLike = SETTINGS.password
) -> Iterator[None]:
    match password:
        case Secret():
            with temp_environ(RESTIC_PASSWORD=password.get_secret_value()):
                yield
        case Path():
            with temp_environ(RESTIC_PASSWORD_FILE=str(password)):
                yield
        case str():
            if Path(password).is_file():
                with temp_environ(RESTIC_PASSWORD_FILE=password):
                    yield
            else:
                with temp_environ(RESTIC_PASSWORD=password):
                    yield


__all__ = ["yield_restic_password"]
