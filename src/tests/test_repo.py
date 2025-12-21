from __future__ import annotations

from typing import TYPE_CHECKING

from hypothesis import given
from typed_settings import Secret
from utilities.hypothesis import paths, text_ascii
from utilities.os import temp_environ

from restic.repo import SFTP, Backblaze

if TYPE_CHECKING:
    from pathlib import Path


class TestBackblaze:
    @given(
        key_id=text_ascii(min_size=1),
        application_key=text_ascii(min_size=1),
        bucket=text_ascii(min_size=1),
        path=paths(min_depth=1),
    )
    def test_main(
        self, *, key_id: str, application_key: str, bucket: str, path: Path
    ) -> None:
        backblaze = Backblaze(Secret(key_id), Secret(application_key), bucket, path)
        with temp_environ(
            BACKBLAZE_KEY_ID=key_id, BACKBLAZE_APPLICATION_KEY=application_key
        ):
            parsed = Backblaze.parse(backblaze.repository)
        assert parsed == backblaze


class TestSFTP:
    @given(
        user=text_ascii(min_size=1),
        hostname=text_ascii(min_size=1),
        path=paths(min_depth=1),
    )
    def test_main(self, *, user: str, hostname: str, path: Path) -> None:
        sftp = SFTP(user, hostname, path)
        assert SFTP.parse(sftp.repository) == sftp
