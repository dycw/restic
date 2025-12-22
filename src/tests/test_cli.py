from __future__ import annotations

from pytest import mark, param
from utilities.subprocess import run


class TestCLI:
    @mark.parametrize(
        ("cmd", "args"),
        [
            param("init", ["local:/tmp"]),
            param("backup", ["path", "local:/tmp"]),
            param("copy", ["local:/tmp", "local:/tmp2"]),
            param("forget", ["local:/tmp"]),
            param("restore", ["local:/tmp", "target"]),
        ],
    )
    def test_main(self, *, cmd: str, args: list[str]) -> None:
        run("py-restic", cmd, *args)
