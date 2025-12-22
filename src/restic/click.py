from __future__ import annotations

from contextlib import suppress
from pathlib import Path
from re import search
from typing import TYPE_CHECKING, assert_never, override

from click import Context, Parameter, ParamType
from utilities.re import ExtractGroupError, ExtractGroupsError

from restic.repo import SFTP, Backblaze, Local

if TYPE_CHECKING:
    import restic.repo


class Repo(ParamType):
    name = "repo"

    @override
    def __repr__(self) -> str:
        return self.name.upper()

    @override
    def convert(
        self, value: restic.repo.Repo, param: Parameter | None, ctx: Context | None
    ) -> restic.repo.Repo:
        match value:
            case Backblaze() | Local() | SFTP() | Path():
                return value
            case str():
                try:
                    return Backblaze.parse(value)
                except ValueError, ExtractGroupsError:
                    if search("b2", value):
                        message = f"For a Backblaze repository {value!r}, the environment varaibles 'BACKBLAZE_KEY_ID' and 'BACKBLAZE_APPLICATION_KEY' must be defined"
                        return self.fail(message, param, ctx)
                with suppress(ExtractGroupsError):
                    return SFTP.parse(value)
                try:
                    return Local.parse(value)
                except ExtractGroupError:
                    return Local(Path(value))
            case never:
                assert_never(never)


__all__ = ["Repo"]
