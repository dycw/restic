from __future__ import annotations

from typing import TYPE_CHECKING

from click import argument, command, echo
from click.testing import CliRunner
from hypothesis import given
from typed_settings import Secret
from utilities.hypothesis import paths, text_ascii
from utilities.os import temp_environ
from utilities.text import strip_and_dedent

import restic.click
import restic.repo
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
        @argument("repo", type=restic.click.Repo())
        def cli(*, repo: restic.repo.Repo) -> None:
            echo(f"repo = {repo}")

        with temp_environ(
            BACKBLAZE_KEY_ID=key_id, BACKBLAZE_APPLICATION_KEY=application_key
        ):
            result = CliRunner().invoke(cli, args=[backblaze.repository])
        assert result.exit_code == 0
        assert result.stdout == f"repo = {backblaze}\n"

    @given(
        key_id=text_ascii(min_size=1),
        application_key=text_ascii(min_size=1),
        bucket=text_ascii(min_size=1),
        path=paths(min_depth=1),
    )
    def test_backblaze_error(
        self, *, key_id: str, application_key: str, bucket: str, path: Path
    ) -> None:
        backblaze = Backblaze(Secret(key_id), Secret(application_key), bucket, path)

        @command()
        @argument("repo", type=restic.click.Repo())
        def cli(*, repo: restic.repo.Repo) -> None:
            echo(f"repo = {repo}")

        result = CliRunner().invoke(cli, args=[backblaze.repository])
        assert result.exit_code == 2
        expected = strip_and_dedent(
            f"""
            Usage: cli [OPTIONS] REPO
            Try 'cli --help' for help.

            Error: Invalid value for 'REPO': For a Backblaze repository {backblaze.repository!r}, the environment varaibles 'BACKBLAZE_KEY_ID' and 'BACKBLAZE_APPLICATION_KEY' must be defined
        """,
            trailing=True,
        )
        assert result.stderr == expected

    @given(
        user=text_ascii(min_size=1),
        hostname=text_ascii(min_size=1),
        path=paths(min_depth=1),
    )
    def test_sftp(self, *, user: str, hostname: str, path: Path) -> None:
        sftp = SFTP(user, hostname, path)

        @command()
        @argument("repo", type=restic.click.Repo())
        def cli(*, repo: restic.repo.Repo) -> None:
            echo(f"repo = {repo}")

        result = CliRunner().invoke(cli, args=[sftp.repository])
        assert result.exit_code == 0
        assert result.stdout == f"repo = {sftp}\n"
