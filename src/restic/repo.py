from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Self, assert_never

from typed_settings import Secret, load_settings
from utilities.os import temp_environ
from utilities.re import extract_groups
from utilities.types import PathLike

from restic.settings import LOADERS, SETTINGS, Settings

if TYPE_CHECKING:
    from collections.abc import Iterator

    from restic.types import SecretLike


type Repo = Backblaze | SFTP | PathLike


@dataclass(order=True, unsafe_hash=True, slots=True)
class Backblaze:
    key_id: Secret[str]
    application_key: Secret[str]
    bucket: str
    path: Path

    @classmethod
    def parse(
        cls,
        text: str,
        /,
        *,
        key_id: SecretLike | None = SETTINGS.backblaze_key_id,
        application_key: SecretLike | None = SETTINGS.backblaze_application_key,
    ) -> Self:
        settings = load_settings(Settings, LOADERS)
        match key_id, settings.backblaze_key_id:
            case Secret() as key_id_use, _:
                ...
            case str(), _:
                key_id_use = Secret(key_id)
            case None, Secret() as key_id_use:
                ...
            case None, None:
                msg = "'BACKBLAZE_KEY_ID' is missing"
                raise ValueError(msg)
            case never:
                assert_never(never)
        match application_key, settings.backblaze_application_key:
            case Secret() as application_key_use, _:
                ...
            case str(), _:
                application_key_use = Secret(application_key)
            case None, Secret() as application_key_use:
                ...
            case None, None:
                msg = "'BACKBLAZE_APPLICATION_KEY' is missing"
                raise ValueError(msg)
            case never:
                assert_never(never)
        bucket, path = extract_groups(r"^b2:([^@:]+):([^@+]+)$", text)
        return cls(key_id_use, application_key_use, bucket, Path(path))

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
            r"^sftp:([^@:]+)@([^@:]+):([^@:]+)$", text
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
        case Path() | str():
            with temp_environ(RESTIC_REPOSITORY=str(repo)):
                yield
        case never:
            assert_never(never)


__all__ = ["SFTP", "Backblaze", "Repo", "yield_repo_env"]
