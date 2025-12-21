from __future__ import annotations

from typed_settings import EnvLoader, Secret, load_settings, option, secret, settings
from utilities.os import CPU_COUNT


@settings(kw_only=True)
class Settings:
    password: Secret[str] = secret(
        default=Secret("password"), help="Repository password"
    )
    read_concurrency: int = option(
        default=max(round(CPU_COUNT / 2), 2), help="Read `n` files concurrency"
    )


SETTINGS = load_settings(Settings, [EnvLoader("")])


__all__ = ["SETTINGS", "Settings"]
