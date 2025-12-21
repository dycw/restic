from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import click
from click import argument, group
from typed_settings import click_options
from utilities.click import CONTEXT_SETTINGS
from utilities.logging import basic_config
from utilities.os import is_pytest

import restic.click
import restic.repo
from restic.lib import backup, forget, init, restore
from restic.logging import LOGGER
from restic.settings import (
    LOADERS,
    BackupSettings,
    ForgetSettings,
    InitSettings,
    RestoreSettings,
)

if TYPE_CHECKING:
    from utilities.types import PathLike


@group(**CONTEXT_SETTINGS)
def _main() -> None: ...


@_main.command(name="init", **CONTEXT_SETTINGS)
@argument("repo", type=restic.click.Repo())
@click_options(InitSettings, LOADERS, show_envvars_in_help=True)
def init_sub_cmd(settings: InitSettings, /, *, repo: restic.repo.Repo) -> None:
    if is_pytest():
        return
    init(repo, password=settings.password)


@_main.command(name="backup", **CONTEXT_SETTINGS)
@argument("path", type=click.Path(path_type=Path))
@argument("repo", type=restic.click.Repo())
@click_options(BackupSettings, LOADERS, show_envvars_in_help=True)
def backup_sub_cmd(
    settings: BackupSettings, /, *, path: PathLike, repo: restic.repo.Repo
) -> None:
    if is_pytest():
        return
    backup(
        path,
        repo,
        chmod=settings.chmod,
        chown=settings.chown,
        password=settings.password,
        dry_run=settings.dry_run,
        exclude=settings.exclude,
        exclude_i=settings.exclude_i,
        read_concurrency=settings.read_concurrency,
        tag_backup=settings.tag_backup,
        run_forget=settings.run_forget,
        keep_last=settings.keep_last,
        keep_hourly=settings.keep_hourly,
        keep_daily=settings.keep_daily,
        keep_weekly=settings.keep_weekly,
        keep_monthly=settings.keep_monthly,
        keep_yearly=settings.keep_yearly,
        keep_within=settings.keep_within,
        keep_within_hourly=settings.keep_within_hourly,
        keep_within_daily=settings.keep_within_daily,
        keep_within_weekly=settings.keep_within_weekly,
        keep_within_monthly=settings.keep_within_monthly,
        keep_within_yearly=settings.keep_within_yearly,
        prune=settings.prune,
        repack_cacheable_only=settings.repack_cacheable_only,
        repack_small=settings.repack_small,
        repack_uncompressed=settings.repack_uncompressed,
        tag_forget=settings.tag_forget,
    )


@_main.command(name="forget", **CONTEXT_SETTINGS)
@argument("repo", type=restic.click.Repo())
@click_options(ForgetSettings, LOADERS, show_envvars_in_help=True)
def forget_sub_cmd(settings: ForgetSettings, /, *, repo: restic.repo.Repo) -> None:
    if is_pytest():
        return
    forget(
        repo,
        password=settings.password,
        dry_run=settings.dry_run,
        keep_last=settings.keep_last,
        keep_hourly=settings.keep_hourly,
        keep_daily=settings.keep_daily,
        keep_weekly=settings.keep_weekly,
        keep_monthly=settings.keep_monthly,
        keep_yearly=settings.keep_yearly,
        keep_within=settings.keep_within,
        keep_within_hourly=settings.keep_within_hourly,
        keep_within_daily=settings.keep_within_daily,
        keep_within_weekly=settings.keep_within_weekly,
        keep_within_monthly=settings.keep_within_monthly,
        keep_within_yearly=settings.keep_within_yearly,
        prune=settings.prune,
        repack_cacheable_only=settings.repack_cacheable_only,
        repack_small=settings.repack_small,
        repack_uncompressed=settings.repack_uncompressed,
        tag=settings.tag,
    )


@_main.command(name="restore", **CONTEXT_SETTINGS)
@argument("repo", type=restic.click.Repo())
@argument("target", type=click.Path(path_type=Path))
@click_options(RestoreSettings, LOADERS, show_envvars_in_help=True)
def restore_sub_cmd(
    settings: RestoreSettings, /, *, repo: restic.repo.Repo, target: PathLike
) -> None:
    if is_pytest():
        return
    restore(
        repo,
        target,
        password=settings.password,
        delete=settings.delete,
        dry_run=settings.dry_run,
        exclude=settings.exclude,
        exclude_i=settings.exclude_i,
        include=settings.include,
        include_i=settings.include_i,
        tag=settings.tag,
        snapshot=settings.snapshot,
    )


if __name__ == "__main__":
    basic_config(obj=LOGGER)
    _main()
