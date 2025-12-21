from __future__ import annotations

from restic import __version__


class TestMain:
    def test_main(self) -> None:
        assert isinstance(__version__, str)
