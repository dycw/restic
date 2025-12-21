from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Self, assert_never

from utilities.os import temp_environ
from utilities.re import extract_groups

if TYPE_CHECKING:
    from collections.abc import Iterator

    from typed_settings import Secret
    from utilities.types import PathLike


type Repo = Backblaze | SFTP | str


@dataclass(order=True, unsafe_hash=True, slots=True)
class Backblaze:
    key_id: Secret[str]
    application_key: Secret[str]
    bucket: str
    path: PathLike

    @property
    def repository(self) -> str:
        return f"b2:{self.bucket}:{self.path}"


@dataclass(order=True, unsafe_hash=True, slots=True)
class SFTP:
    user: str
    hostname: str
    path: Path

    @classmethod
    def parse(cls, text: str, /) -> Self:
        user, hostname, path = extract_groups(
            r"^sftp:([A-Za-z0-9]+)@([A-Za-z0-9]+):([A-Za-z0-9/]+)$", text
        )
        return cls(user, hostname, Path(path))

    @property
    def repository(self) -> str:
        return f"sftp:{self.user}@{self.hostname}:{self.path}"


@contextmanager
def yield_repo_env(repo: Repo, /) -> Iterator[None]:
    match repo:
        case Backblaze():
            with temp_environ(
                B2_ACCOUNT_ID=repo.key_id.get_secret_value(),
                B2_ACCOUNT_KEY=repo.application_key.get_secret_value(),
                RESTIC_REPOSITORY=repo.repository,
            ):
                yield
        case SFTP():
            with temp_environ(RESTIC_REPOSITORY=repo.repository):
                yield
        case str():
            with temp_environ(RESTIC_REPOSITORY=repo):
                yield
        case never:
            assert_never(never)


__all__ = ["SFTP", "Backblaze", "Repo", "yield_repo_env"]
