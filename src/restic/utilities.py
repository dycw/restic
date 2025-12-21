from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from typed_settings import Secret
from utilities.os import temp_environ
from utilities.subprocess import run

from restic.settings import SETTINGS

if TYPE_CHECKING:
    from collections.abc import Iterator

    from utilities.types import PathLike

    from restic.types import PasswordLike


def run_chmod(path: PathLike, type_: Literal["f", "d"], mode: str, /) -> None:
    run("sudo", "find", str(path), "-type", type_, "-exec", "chmod", mode, "{}", "+")


@contextmanager
def yield_password(*, password: PasswordLike = SETTINGS.password) -> Iterator[None]:
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


__all__ = ["run_chmod", "yield_password"]
