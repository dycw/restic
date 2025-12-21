from __future__ import annotations

from inspect import getattr_static
from operator import ge
from typing import TYPE_CHECKING

from attrs import fields_dict
from click import argument, group, option
from rich.pretty import pretty_repr
from typed_settings import EnvLoader, click_options
from utilities.click import CONTEXT_SETTINGS
from utilities.logging import basic_config

import restic.click
import restic.repo
from restic.lib import init
from restic.logging import LOGGER
from restic.settings import SETTINGS, Settings

if TYPE_CHECKING:
    from restic.types import SecretLike


@group(**CONTEXT_SETTINGS)
def _main() -> None: ...


@_main.command(name="init", **CONTEXT_SETTINGS)
@argument("repo", type=restic.click.Repo())
@option(
    "--password",
    type=str,
    default=SETTINGS.password,
    help=Settings.get_help(Settings.password),
)
def init_sub_cmd(*, repo: restic.repo.Repo, password: SecretLike) -> None:
    init(repo, password=password)


if __name__ == "__main__":
    basic_config(obj=LOGGER)
    _main()
