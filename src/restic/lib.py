from __future__ import annotations

from re import MULTILINE, search
from subprocess import CalledProcessError
from typing import TYPE_CHECKING

from utilities.subprocess import run

from restic.logging import LOGGER
from restic.repo import yield_repo_env
from restic.settings import SETTINGS
from restic.utilities import (
    expand_bool,
    expand_dry_run,
    expand_exclude,
    expand_exclude_i,
    expand_include,
    expand_include_i,
    expand_keep,
    expand_keep_within,
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
    chmod: bool = SETTINGS.chmod,
    chown: str | None = SETTINGS.chown,
    password: PasswordLike = SETTINGS.password,
    dry_run: bool = SETTINGS.dry_run,
    exclude: list[str] | None = None,
    iexclude: list[str] | None = None,
    read_concurrency: int = SETTINGS.read_concurrency,
    tag_backup: list[str] | None = SETTINGS.tag_backup,
    run_forget: bool = SETTINGS.run_forget,
    keep_last: int | None = SETTINGS.keep_last,
    keep_hourly: int | None = SETTINGS.keep_hourly,
    keep_daily: int | None = SETTINGS.keep_daily,
    keep_weekly: int | None = SETTINGS.keep_weekly,
    keep_monthly: int | None = SETTINGS.keep_monthly,
    keep_yearly: int | None = SETTINGS.keep_yearly,
    keep_within: str | None = SETTINGS.keep_within,
    keep_within_hourly: str | None = SETTINGS.keep_within_hourly,
    keep_within_daily: str | None = SETTINGS.keep_within_daily,
    keep_within_weekly: str | None = SETTINGS.keep_within_weekly,
    keep_within_monthly: str | None = SETTINGS.keep_within_monthly,
    keep_within_yearly: str | None = SETTINGS.keep_within_yearly,
    prune: bool = SETTINGS.prune,
    repack_cacheable_only: bool = SETTINGS.repack_cacheable_only,
    repack_small: bool = SETTINGS.repack_small,
    repack_uncompressed: bool = SETTINGS.repack_uncompressed,
    tag_forget: list[str] | None = SETTINGS.tag_forget,
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
            tag=tag_backup,
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
                tag=tag_backup,
            )
        else:
            raise
    if run_forget:
        forget(
            repo,
            password=password,
            keep_last=keep_last,
            keep_hourly=keep_hourly,
            keep_daily=keep_daily,
            keep_weekly=keep_weekly,
            keep_monthly=keep_monthly,
            keep_yearly=keep_yearly,
            keep_within=keep_within,
            keep_within_hourly=keep_within_hourly,
            keep_within_daily=keep_within_daily,
            keep_within_weekly=keep_within_weekly,
            keep_within_monthly=keep_within_monthly,
            keep_within_yearly=keep_within_yearly,
            prune=prune,
            repack_cacheable_only=repack_cacheable_only,
            repack_small=repack_small,
            repack_uncompressed=repack_uncompressed,
            tag=tag_forget,
        )
    LOGGER.info("Finished backing up '%s' to '%s'", path, repo)


def _backup_core(
    path: PathLike,
    repo: Repo,
    /,
    *,
    password: PasswordLike = SETTINGS.password,
    dry_run: bool = SETTINGS.dry_run,
    exclude: list[str] | None = None,
    iexclude: list[str] | None = None,
    read_concurrency: int = SETTINGS.read_concurrency,
    tag: list[str] | None = SETTINGS.tag_backup,
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


def forget(
    repo: Repo,
    /,
    *,
    password: PasswordLike = SETTINGS.password,
    dry_run: bool = SETTINGS.dry_run,
    keep_last: int | None = SETTINGS.keep_last,
    keep_hourly: int | None = SETTINGS.keep_hourly,
    keep_daily: int | None = SETTINGS.keep_daily,
    keep_weekly: int | None = SETTINGS.keep_weekly,
    keep_monthly: int | None = SETTINGS.keep_monthly,
    keep_yearly: int | None = SETTINGS.keep_yearly,
    keep_within: str | None = SETTINGS.keep_within,
    keep_within_hourly: str | None = SETTINGS.keep_within_hourly,
    keep_within_daily: str | None = SETTINGS.keep_within_daily,
    keep_within_weekly: str | None = SETTINGS.keep_within_weekly,
    keep_within_monthly: str | None = SETTINGS.keep_within_monthly,
    keep_within_yearly: str | None = SETTINGS.keep_within_yearly,
    prune: bool = SETTINGS.prune,
    repack_cacheable_only: bool = SETTINGS.repack_cacheable_only,
    repack_small: bool = SETTINGS.repack_small,
    repack_uncompressed: bool = SETTINGS.repack_uncompressed,
    tag: list[str] | None = SETTINGS.tag_forget,
) -> None:
    LOGGER.info("Forgetting snapshots in '%s'...", repo)
    with yield_repo_env(repo), yield_password(password=password):
        run(
            "restic",
            "forget",
            *expand_dry_run(dry_run=dry_run),
            *expand_keep("last", n=keep_last),
            *expand_keep("hourly", n=keep_hourly),
            *expand_keep("daily", n=keep_daily),
            *expand_keep("weekly", n=keep_weekly),
            *expand_keep("monthly", n=keep_monthly),
            *expand_keep("yearly", n=keep_yearly),
            *expand_keep_within("within", duration=keep_within),
            *expand_keep_within("within-hourly", duration=keep_within_hourly),
            *expand_keep_within("within-daily", duration=keep_within_daily),
            *expand_keep_within("within-weekly", duration=keep_within_weekly),
            *expand_keep_within("within-monthly", duration=keep_within_monthly),
            *expand_keep_within("within-yearly", duration=keep_within_yearly),
            *expand_bool("prune", bool_=prune),
            *expand_bool("repack-cacheable-only", bool_=repack_cacheable_only),
            *expand_bool("repack-small", bool_=repack_small),
            *expand_bool("repack-uncompressed", bool_=repack_uncompressed),
            *expand_tag(tag=tag),
        )
    LOGGER.info("Finished forgetting snapshots in '%s'", repo)


def restore(
    repo: Repo,
    target: PathLike,
    /,
    *,
    password: PasswordLike = SETTINGS.password,
    delete: bool = False,
    dry_run: bool = SETTINGS.dry_run,
    exclude: list[str] | None = None,
    exclude_i: list[str] | None = None,
    include: list[str] | None = None,
    include_i: list[str] | None = None,
    tag: list[str] | None = SETTINGS.tag_restore,
    snapshot: str = "latest",
) -> None:
    LOGGER.info("Restoring snapshot '%s' of '%s' to '%s'...", snapshot, repo, target)
    with yield_repo_env(repo), yield_password(password=password):
        run(
            "restic",
            "restore",
            *expand_bool("delete", bool_=delete),
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


__all__ = ["backup", "forget", "init", "restore"]
