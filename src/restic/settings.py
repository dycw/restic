from __future__ import annotations

from typed_settings import EnvLoader, Secret, load_settings, option, secret, settings
from utilities.os import CPU_COUNT


@settings(kw_only=True)
class Settings:
    # global
    dry_run: bool = option(default=False, help="Just print what would have backup done")
    password: Secret[str] = secret(
        default=Secret("password"), help="Repository password"
    )
    # backup
    read_concurrency: int = option(
        default=max(round(CPU_COUNT / 2), 2), help="Read `n` files concurrency"
    )
    run_forget: bool = option(
        default=True, help="Automatically run the 'forget' command"
    )
    # forget
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


SETTINGS = load_settings(Settings, [EnvLoader("")])


__all__ = ["SETTINGS", "Settings"]
