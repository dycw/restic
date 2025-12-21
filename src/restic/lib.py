from __future__ import annotations

from itertools import chain
from re import MULTILINE, search
from subprocess import CalledProcessError
from typing import TYPE_CHECKING

from utilities.subprocess import run

from restic.logging import LOGGER
from restic.repo import yield_repo_env
from restic.settings import SETTINGS
from restic.utilities import run_chmod, yield_password

if TYPE_CHECKING:
    from utilities.types import PathLike

    from restic.repo import Repo
    from restic.types import PasswordLike


def backup(
    path: PathLike,
    repo: Repo,
    /,
    *,
    chmod: bool = False,
    chown: str | None = None,
    password: PasswordLike = SETTINGS.password,
    dry_run: bool = False,
    exclude: list[str] | None = None,
    tags: list[str] | None = None,
) -> None:
    LOGGER.info("Backing up '%s' to '%s'...", path, repo)
    if chmod:
        run_chmod(path, "d", "u=rwx,g=rx,o=rx")
        run_chmod(path, "f", "u=rw,g=r,o=r")
    if chown is not None:
        run("sudo", "chown", "-R", f"{chown}:{chown}", str(path))
    try:
        _backup_core(
            path, repo, password=password, dry_run=dry_run, exclude=exclude, tags=tags
        )
    except CalledProcessError as error:
        if search(
            "Is there a repository at the following location?",
            error.stderr,
            flags=MULTILINE,
        ):
            LOGGER.info("Auto-initializing repo...")
            init(repo, password=password)
            _backup_core(
                path,
                repo,
                password=password,
                dry_run=dry_run,
                exclude=exclude,
                tags=tags,
            )
        else:
            raise
    LOGGER.info("Finished backing up '%s' to '%s'", path, repo)


def _backup_core(
    path: PathLike,
    repo: Repo,
    /,
    *,
    password: PasswordLike = SETTINGS.password,
    dry_run: bool = False,
    exclude: list[str] | None = None,
    tags: list[str] | None = None,
) -> None:
    with yield_repo_env(repo), yield_password(password=password):
        run(
            "restic",
            "backup",
            *(["--dry-run"] if dry_run else []),
            *(
                []
                if exclude is None
                else chain.from_iterable(["--exclude", e] for e in exclude)
            ),
            *([] if tags is None else chain.from_iterable(["--tag", t] for t in tags)),
            str(path),
        )


def init(repo: Repo, /, *, password: PasswordLike = SETTINGS.password) -> None:
    LOGGER.info("Initializing '%s'", repo)
    with yield_repo_env(repo), yield_password(password=password):
        run("restic", "init")
    LOGGER.info("Finished initializing '%s'", repo)


__all__ = ["backup", "init"]
