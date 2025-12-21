from __future__ import annotations

import typed_settings
from typed_settings import EnvLoader, Secret, load_settings, secret, settings


@settings(kw_only=True)
class Settings:
    password: Secret[str] = secret(
        default=Secret("password"), help="Repository password"
    )
    backup: Backup
    restic: Restic
    truenas: TrueNAS
    dry_run: bool = typed_settings.option(default=False, help="Dry run the CLI")


SETTINGS = load_settings(Settings, [EnvLoader("")])


__all__ = ["SETTINGS", "Settings"]
