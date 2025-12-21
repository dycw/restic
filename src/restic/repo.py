from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, assert_never

from utilities.os import temp_environ

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
    path: PathLike

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
