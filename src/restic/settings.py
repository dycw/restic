from __future__ import annotations

from typing import Any

from attrs import fields_dict
from typed_settings import (
    EnvLoader,
    FileLoader,
    Secret,
    TomlFormat,
    find,
    load_settings,
    option,
    secret,
    settings,
)
from utilities.os import CPU_COUNT

LOADERS = [
    FileLoader(
        {"*.toml": TomlFormat(None)}, [find("config.toml"), find("secrets.toml")]
    ),
    EnvLoader(""),
]


@settings(kw_only=True)
class Settings:
    # global
    dry_run: bool = option(default=False, help="Just print what would have been done")
    password: Secret[str] = secret(
        default=Secret("password"), help="Repository password"
    )
    # backblaze
    backblaze_key_id: Secret[str] | None = secret(default=None, help="Backblaze key ID")
    backblaze_application_key: Secret[str] | None = secret(
        default=None, help="Backblaze application key"
    )
    # backup
    chmod: bool = option(default=False, help="Change permissions of the directory/file")
    chown: str | None = option(
        default=None, help="Change ownership of the directory/file"
    )
    read_concurrency: int = option(
        default=max(round(CPU_COUNT / 2), 2), help="Read `n` files concurrency"
    )
    tag_backup: list[str] = option(
        factory=list, help="Add tags for the snapshot in the format `tag[,tag,...]`"
    )
    run_forget: bool = option(
        default=True, help="Automatically run the 'forget' command"
    )
    # forget
    keep_last: int | None = option(default=None, help="Keep the last n snapshots")
    keep_hourly: int | None = option(
        default=None, help="Keep the last n hourly snapshots"
    )
    keep_daily: int | None = option(
        default=None, help="Keep the last n daily snapshots"
    )
    keep_weekly: int | None = option(
        default=None, help="Keep the last n weekly snapshots"
    )
    keep_monthly: int | None = option(
        default=None, help="Keep the last n monthly snapshots"
    )
    keep_yearly: int | None = option(
        default=None, help="Keep the last n yearly snapshots"
    )
    keep_within: str | None = option(
        default=None,
        help="Keep snapshots that are newer than duration relative to the latest snapshot",
    )
    keep_within_hourly: str | None = option(
        default=None,
        help="Keep hourly snapshots that are newer than duration relative to the latest snapshot",
    )
    keep_within_daily: str | None = option(
        default=None,
        help="Keep daily snapshots that are newer than duration relative to the latest snapshot",
    )
    keep_within_weekly: str | None = option(
        default=None,
        help="Keep weekly snapshots that are newer than duration relative to the latest snapshot",
    )
    keep_within_monthly: str | None = option(
        default=None,
        help="Keep monthly snapshots that are newer than duration relative to the latest snapshot",
    )
    keep_within_yearly: str | None = option(
        default=None,
        help="Keep yearly snapshots that are newer than duration relative to the latest snapshot",
    )
    prune: bool = option(
        default=True,
        help="Automatically run the 'prune' command if snapshots have been removed",
    )
    repack_cacheable_only: bool = option(
        default=False, help="Only repack packs which are cacheable"
    )
    repack_small: bool = option(
        default=True, help="Repack pack files below 80% of target pack size"
    )
    repack_uncompressed: bool = option(
        default=False, help="Repack all uncompressed data"
    )
    tag_forget: list[str] | None = option(
        factory=list, help="Only consider snapshots including tag[,tag,...]"
    )
    # restore
    tag_restore: list[str] | None = option(
        factory=list,
        help='Only consider snapshots including tag[,tag,...], when snapshot ID "latest" is given',
    )


SETTINGS = load_settings(Settings, LOADERS)


def _get_help(member_descriptor: Any, /) -> None:
    return fields_dict(Settings)[member_descriptor.__name__].metadata["typed-settings"][
        "help"
    ]


@settings(kw_only=True)
class InitSettings:
    password: Secret[str] = secret(
        default=SETTINGS.password, help=_get_help(Settings.password)
    )


@settings(kw_only=True)
class BackupSettings:
    chmod: bool = option(default=SETTINGS.chmod, help=_get_help(Settings.chmod))
    chown: str | None = option(default=SETTINGS.chown, help=_get_help(Settings.chown))
    password: Secret[str] = secret(
        default=SETTINGS.password, help=_get_help(Settings.password)
    )
    dry_run: bool = option(default=SETTINGS.dry_run, help=_get_help(Settings.dry_run))
    read_concurrency: int = option(
        default=SETTINGS.read_concurrency, help=_get_help(Settings.read_concurrency)
    )
    tag: list[str] = option(factory=list, help=_get_help(Settings.tag_backup))
    run_forget: bool = option(
        default=SETTINGS.run_forget, help=_get_help(Settings.run_forget)
    )
    keep_last: int | None = option(
        default=SETTINGS.keep_last, help=_get_help(Settings.keep_last)
    )
    keep_hourly: int | None = option(
        default=SETTINGS.keep_hourly, help=_get_help(Settings.keep_hourly)
    )
    keep_daily: int | None = option(
        default=SETTINGS.keep_daily, help=_get_help(Settings.keep_daily)
    )
    keep_weekly: int | None = option(
        default=SETTINGS.keep_weekly, help=_get_help(Settings.keep_weekly)
    )
    keep_monthly: int | None = option(
        default=SETTINGS.keep_monthly, help=_get_help(Settings.keep_monthly)
    )
    keep_yearly: int | None = option(
        default=SETTINGS.keep_yearly, help=_get_help(Settings.keep_yearly)
    )
    keep_within: str | None = option(
        default=SETTINGS.keep_within, help=_get_help(Settings.keep_within)
    )
    keep_within_z: str | None = option(
        default=SETTINGS.keep_within_z, help=_get_help(Settings.keep_within_z)
    )
    keep_within_z: str | None = option(
        default=SETTINGS.keep_within_z, help=_get_help(Settings.keep_within_z)
    )
    keep_within_z: str | None = option(
        default=SETTINGS.keep_within_z, help=_get_help(Settings.keep_within_z)
    )
    keep_within_z: str | None = option(
        default=SETTINGS.keep_within_z, help=_get_help(Settings.keep_within_z)
    )
    keep_within_z: str | None = option(
        default=SETTINGS.keep_within_z, help=_get_help(Settings.keep_within_z)
    )
    keep_within_z: str | None = option(
        default=SETTINGS.keep_within_z, help=_get_help(Settings.keep_within_z)
    )
    z: bool = option(default=SETTINGS.z, help=_get_help(Settings.z))
    z: bool = option(default=SETTINGS.z, help=_get_help(Settings.z))
    z: bool = option(default=SETTINGS.z, help=_get_help(Settings.z))
    z: bool = option(default=SETTINGS.z, help=_get_help(Settings.z))
    z: bool = option(default=SETTINGS.z, help=_get_help(Settings.z))
    z: bool = option(default=SETTINGS.z, help=_get_help(Settings.z))
    # z: bool = option(default=SETTINGS.z, help=_get_help(Settings.z))


__all__ = ["LOADERS", "SETTINGS", "BackupSettings", "InitSettings", "Settings"]
