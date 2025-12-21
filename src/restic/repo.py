from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, assert_never

if TYPE_CHECKING:
    from utilities.types import PathLike


type Repo = Backblaze | SFTP | str


@dataclass(order=True, unsafe_hash=True, slots=True)
class Backblaze:
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


def ensure_repo(repo: Repo, /) -> str:
    match repo:
        case Backblaze() | SFTP():
            return repo.repository
        case str():
            return repo
        case never:
            assert_never(never)


__all__ = ["SFTP", "Backblaze", "Repo", "ensure_repo"]
