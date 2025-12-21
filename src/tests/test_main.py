from __future__ import annotations

from pytest import mark, param
from utilities.subprocess import run


class TestCLI:
    @mark.parametrize(("cmd", "args"), [param("restore", ["repo", "target"])])
    def test_main(self, *, cmd: str, args: list[str]) -> None:
        run("py-restic", cmd, *args)
