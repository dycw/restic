from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, assert_never, override

from click import Context, Parameter, ParamType
from utilities.re import ExtractGroupsError

from restic.repo import SFTP, Backblaze

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
            case Backblaze() | SFTP():
                return value
            case str():
                with suppress(ValueError, ExtractGroupsError):
                    return Backblaze.parse(value)
                with suppress(ExtractGroupsError):
                    return SFTP.parse(value)
                return self.fail(f"Unable to parse {value!r}", param, ctx)
            case never:
                assert_never(never)


__all__ = ["Repo"]
