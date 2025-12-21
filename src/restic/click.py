from __future__ import annotations

import enum
import ipaddress
import pathlib
import uuid
from enum import StrEnum
from re import search
from typing import TYPE_CHECKING, TypedDict, assert_never, override

import whenever
from click import Choice, Context, Parameter, ParamType
from click.types import IntParamType, StringParamType
from utilities.enum import EnsureEnumError, ensure_enum
from utilities.functions import EnsureStrError, ensure_str, get_class, get_class_name
from utilities.iterables import is_iterable_not_str, one_unique
from utilities.parse import ParseObjectError, parse_object
from utilities.re import extract_group
from utilities.text import split_str

from restic.repo import SFTP, Backblaze

if TYPE_CHECKING:
    from collections.abc import Iterable

    from utilities.types import (
        DateDeltaLike,
        DateLike,
        DateTimeDeltaLike,
        EnumLike,
        IPv4AddressLike,
        IPv6AddressLike,
        MaybeStr,
        MonthDayLike,
        PathLike,
        PlainDateTimeLike,
        TimeDeltaLike,
        TimeLike,
        YearMonthLike,
        ZonedDateTimeLike,
    )

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
                try:
                    return whenever.DateDelta.parse_iso(value)
                except ValueError as error:
                    self.fail(str(error), param, ctx)
            case never:
                assert_never(never)
        return None
