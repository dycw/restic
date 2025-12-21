from __future__ import annotations

from typing import TYPE_CHECKING

from hypothesis import given
from utilities.hypothesis import paths, text_ascii

from restic.repo import SFTP

if TYPE_CHECKING:
    from pathlib import Path


class TestSFTP:
    @given(
        user=text_ascii(min_size=1),
        hostname=text_ascii(min_size=1),
        path=paths(min_depth=1),
    )
    def test_main(self, *, user: str, hostname: str, path: Path) -> None:
        sftp = SFTP(user, hostname, path)
        assert SFTP.parse(sftp.repository) == sftp
