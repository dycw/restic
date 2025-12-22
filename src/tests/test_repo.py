from __future__ import annotations

from pathlib import Path

from hypothesis import given
from pytest import raises
from typed_settings import Secret
from utilities.hypothesis import paths, text_ascii
from utilities.os import temp_environ

from restic.repo import SFTP, Backblaze, Local, parse_repo


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
            repo = Backblaze.parse(backblaze.repository)
        assert repo == backblaze


class TestLocal:
    @given(path=paths(min_depth=1))
    def test_main(self, *, path: Path) -> None:
        repo = Local(path)
        parsed = Local.parse(repo.repository)
        assert parsed == repo


class TestParseRepo:
    @given(
        key_id=text_ascii(min_size=1),
        application_key=text_ascii(min_size=1),
        bucket=text_ascii(min_size=1),
        path=paths(min_depth=1),
    )
    def test_backblaze(
        self, *, key_id: str, application_key: str, bucket: str, path: Path
    ) -> None:
        repo = Backblaze(Secret(key_id), Secret(application_key), bucket, path)
        with temp_environ(
            BACKBLAZE_KEY_ID=key_id, BACKBLAZE_APPLICATION_KEY=application_key
        ):
            parsed = parse_repo(repo.repository)
        assert isinstance(parsed, Backblaze)
        assert parsed == repo

    @given(
        key_id=text_ascii(min_size=1),
        application_key=text_ascii(min_size=1),
        bucket=text_ascii(min_size=1),
        path=paths(min_depth=1),
    )
    def test_backblaze_error(
        self, *, key_id: str, application_key: str, bucket: str, path: Path
    ) -> None:
        repo = Backblaze(Secret(key_id), Secret(application_key), bucket, path)
        with raises(
            ValueError,
            match=f"For a Backblaze repository {repo.repository!r}, the environment varaibles 'BACKBLAZE_KEY_ID' and 'BACKBLAZE_APPLICATION_KEY' must be defined",
        ):
            _ = parse_repo(repo.repository)

    @given(path=paths(min_depth=1))
    def test_local(self, *, path: Path) -> None:
        repo = Local(path)
        parsed = parse_repo(repo.repository)
        assert isinstance(parsed, Local)
        assert parsed == repo

    @given(
        user=text_ascii(min_size=1),
        hostname=text_ascii(min_size=1),
        path=paths(min_depth=1),
    )
    def test_sftp(self, *, user: str, hostname: str, path: Path) -> None:
        repo = SFTP(user, hostname, path)
        parsed = parse_repo(repo.repository)
        assert isinstance(parsed, SFTP)
        assert parsed == repo

    @given(text=text_ascii(min_size=1))
    def test_regular_text(self, *, text: str) -> None:
        parsed = parse_repo(text)
        assert isinstance(parsed, Local)
        expected = Local(Path(text))
        assert parsed == expected


class TestSFTP:
    @given(
        user=text_ascii(min_size=1),
        hostname=text_ascii(min_size=1),
        path=paths(min_depth=1),
    )
    def test_main(self, *, user: str, hostname: str, path: Path) -> None:
        repo = SFTP(user, hostname, path)
        assert SFTP.parse(repo.repository) == repo
