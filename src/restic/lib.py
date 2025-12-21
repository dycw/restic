from __future__ import annotations

from re import MULTILINE, search
from subprocess import CalledProcessError
from typing import TYPE_CHECKING

from utilities.subprocess import run

from restic.logging import LOGGER
from restic.repo import yield_repo_env
from restic.settings import SETTINGS
from restic.utilities import (
    expand_dry_run,
    expand_exclude,
    expand_exclude_i,
    expand_include,
    expand_include_i,
    expand_tag,
    run_chmod,
    yield_password,
)

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
    iexclude: list[str] | None = None,
    read_concurrency: int = SETTINGS.read_concurrency,
    tag: list[str] | None = None,
) -> None:
    LOGGER.info("Backing up '%s' to '%s'...", path, repo)
    if chmod:
        run_chmod(path, "d", "u=rwx,g=rx,o=rx")
        run_chmod(path, "f", "u=rw,g=r,o=r")
    if chown is not None:
        run("sudo", "chown", "-R", f"{chown}:{chown}", str(path))
    try:
        _backup_core(
            path,
            repo,
            password=password,
            dry_run=dry_run,
            exclude=exclude,
            iexclude=iexclude,
            read_concurrency=read_concurrency,
            tag=tag,
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
                iexclude=iexclude,
                read_concurrency=read_concurrency,
                tag=tag,
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
    iexclude: list[str] | None = None,
    read_concurrency: int = SETTINGS.read_concurrency,
    tag: list[str] | None = None,
) -> None:
    with yield_repo_env(repo), yield_password(password=password):
        run(
            "restic",
            "backup",
            *expand_dry_run(dry_run=dry_run),
            *expand_exclude(exclude=exclude),
            *expand_exclude_i(exclude_i=iexclude),
            "--read-conconcurrency",
            str(read_concurrency),
            *expand_tag(tag=tag),
            str(path),
        )


def init(repo: Repo, /, *, password: PasswordLike = SETTINGS.password) -> None:
    LOGGER.info("Initializing '%s'", repo)
    with yield_repo_env(repo), yield_password(password=password):
        run("restic", "init")
    LOGGER.info("Finished initializing '%s'", repo)


def restore(
    repo: Repo,
    target: PathLike,
    /,
    *,
    password: PasswordLike = SETTINGS.password,
    delete: bool = False,
    dry_run: bool = False,
    exclude: list[str] | None = None,
    exclude_i: list[str] | None = None,
    include: list[str] | None = None,
    include_i: list[str] | None = None,
    tag: list[str] | None = None,
    snapshot: str = "latest",
) -> None:
    LOGGER.info("Restoring snapshot '%s' of '%s' to '%s'...", snapshot, repo, target)
    with yield_repo_env(repo), yield_password(password=password):
        run(
            "restic",
            "restore",
            *(["--delete"] if delete else []),
            *expand_dry_run(dry_run=dry_run),
            *expand_exclude(exclude=exclude),
            *expand_exclude_i(exclude_i=exclude_i),
            *expand_include(include=include),
            *expand_include_i(include_i=include_i),
            *expand_tag(tag=tag),
            "--target",
            str(target),
            "--verify",
            snapshot,
        )
    LOGGER.info(
        "Finished restoring snapshot '%s' of '%s' to '%s'", snapshot, repo, target
    )


__all__ = ["backup", "init", "restore"]
