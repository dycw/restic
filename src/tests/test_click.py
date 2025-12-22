from __future__ import annotations

from typing import TYPE_CHECKING

from click import argument, command, echo, option
from click.testing import CliRunner
from hypothesis import given
from typed_settings import Secret
from utilities.hypothesis import paths, text_ascii
from utilities.os import temp_environ

import restic.click
import restic.repo
from restic.click import Repo
from restic.repo import SFTP, Backblaze

if TYPE_CHECKING:
    from pathlib import Path


class TestRepo:
    @given(
        key_id=text_ascii(min_size=1),
        application_key=text_ascii(min_size=1),
        bucket=text_ascii(min_size=1),
        path=paths(min_depth=1),
    )
    def test_backblaze(
        self, *, key_id: str, application_key: str, bucket: str, path: Path
    ) -> None:
        backblaze = Backblaze(Secret(key_id), Secret(application_key), bucket, path)

        @command()
        @argument("value", type=restic.click.Repo())
        def cli(*, value: restic.repo.Repo) -> None:
            echo(f"value = {value}")

        with temp_environ(
            BACKBLAZE_KEY_ID=key_id, BACKBLAZE_APPLICATION_KEY=application_key
        ):
            result = CliRunner().invoke(cli, args=[backblaze.repository])
        assert result.exit_code == 0, [result.stdout, result.stderr]
        assert result.stdout == f"value = {backblaze}\n"
