from __future__ import annotations

from click import argument, command, group
from rich.pretty import pretty_repr
from typed_settings import EnvLoader, click_options
from utilities.click import CONTEXT_SETTINGS
from utilities.logging import basic_config

from restic.lib import init, restic
from restic.logging import LOGGER
from restic.settings import Settings


@group(**CONTEXT_SETTINGS)
def _main() -> None: ...


@_main.command(name="init", **CONTEXT_SETTINGS)
@argument("repo", type=str)
def init_sub_cmd() -> None:
    init()


@group(**CONTEXT_SETTINGS)
@click_options(Settings, [EnvLoader("")], show_envvars_in_help=True)
def _main(settings: Settings, /) -> None:
    LOGGER.info("Settings = %s", pretty_repr(settings))
    if settings.dry_run:
        LOGGER.info("Dry-run; exiting...")
        return
    restic(
        name=settings.name,
        prepend_path=settings.prepend_path,
        schedule=settings.schedule,
        user=settings.user,
        timeout=settings.timeout,
        kill_after=settings.kill_after,
        path_script=settings.path_script,
        script_args=settings.script_args,
        logs_keep=settings.logs_keep,
    )


if __name__ == "__main__":
    basic_config(obj=LOGGER)
    _main()
