from __future__ import annotations

from pytest import mark, param
from utilities.subprocess import run


class TestCLI:
    @mark.parametrize(
        ("cmd", "args"),
        [
            param("init", ["sftp:user@hostname:/tmp"]),
            param("backup", ["path", "sftp:user@hostname:/tmp"]),
            param("forget", ["sftp:user@hostname:/tmp"]),
            param("restore", ["sftp:user@hostname:/tmp", "target"]),
        ],
    )
    def test_main(self, *, cmd: str, args: list[str]) -> None:
        run("py-restic", cmd, *args)
