"""Original-byte source locations and cursor advancement."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True, slots=True)
class SourceSpan:
    """A zero-based half-open byte span in the original source."""

    start_byte: int
    end_byte: int

    def __post_init__(self) -> None:
        if self.start_byte < 0:
            raise ValueError("start_byte must be nonnegative")
        if self.end_byte < self.start_byte:
            raise ValueError("end_byte must not precede start_byte")

    @property
    def byte_length(self) -> int:
        return self.end_byte - self.start_byte


@dataclass(frozen=True, slots=True)
class SourcePosition:
    """A byte offset plus its one-based logical line and display column."""

    byte_offset: int
    line: int
    column: int

    def __post_init__(self) -> None:
        if self.byte_offset < 0:
            raise ValueError("byte_offset must be nonnegative")
        if self.line < 1:
            raise ValueError("line must be at least one")
        if self.column < 1:
            raise ValueError("column must be at least one")


@dataclass(frozen=True, slots=True)
class PositionRange:
    """Human-readable positions for the boundaries of a byte span."""

    start: SourcePosition
    end: SourcePosition

    def __post_init__(self) -> None:
        if self.end.byte_offset < self.start.byte_offset:
            raise ValueError("end position must not precede start position")

    @property
    def span(self) -> SourceSpan:
        return SourceSpan(self.start.byte_offset, self.end.byte_offset)


class SourceUnitKind(Enum):
    """The location-relevant unit consumed by one cursor step."""

    ASCII = "ASCII"
    TAB = "TAB"
    NEWLINE = "NEWLINE"
    UNICODE = "UNICODE"
    INVALID_UTF8 = "INVALID_UTF8"


@dataclass(frozen=True, slots=True)
class SourceUnit:
    """One consumed logical source unit and its unchanged source bytes."""

    kind: SourceUnitKind
    source_bytes: bytes
    positions: PositionRange

    @property
    def span(self) -> SourceSpan:
        return self.positions.span

    @property
    def text(self) -> str | None:
        if self.kind is SourceUnitKind.INVALID_UTF8:
            return None
        return self.source_bytes.decode("utf-8")


class SourceCursor:
    """Advance through original bytes without normalizing or pre-decoding them."""

    __slots__ = ("_source", "_offset", "_line", "_column")

    def __init__(self, source: bytes) -> None:
        if not isinstance(source, bytes):
            raise TypeError("source must be bytes")
        self._source = source
        self._offset = 0
        self._line = 1
        self._column = 1

    @property
    def source(self) -> bytes:
        return self._source

    @property
    def offset(self) -> int:
        return self._offset

    @property
    def at_end(self) -> bool:
        return self._offset == len(self._source)

    @property
    def position(self) -> SourcePosition:
        return SourcePosition(self._offset, self._line, self._column)

    def peek_byte(self, distance: int = 0) -> int | None:
        if distance < 0:
            raise ValueError("distance must be nonnegative")
        index = self._offset + distance
        if index >= len(self._source):
            return None
        return self._source[index]

    def utf8_scalar_length(self) -> int | None:
        """Return the valid scalar width at the cursor, or ``None`` if invalid."""

        return _utf8_scalar_length(self._source, self._offset)

    def advance(self) -> SourceUnit:
        """Consume one location-relevant unit, always making byte progress."""

        if self.at_end:
            raise EOFError("cannot advance beyond physical EOF")

        start = self.position
        first = self._source[self._offset]

        if first == 0x0D:
            width = 2 if self.peek_byte(1) == 0x0A else 1
            kind = SourceUnitKind.NEWLINE
            self._offset += width
            self._line += 1
            self._column = 1
        elif first == 0x0A:
            width = 1
            kind = SourceUnitKind.NEWLINE
            self._offset += 1
            self._line += 1
            self._column = 1
        elif first == 0x09:
            width = 1
            kind = SourceUnitKind.TAB
            self._offset += 1
            self._column += 4 - ((self._column - 1) % 4)
        else:
            scalar_length = self.utf8_scalar_length()
            if scalar_length is None:
                width = 1
                kind = SourceUnitKind.INVALID_UTF8
            elif scalar_length == 1:
                width = 1
                kind = SourceUnitKind.ASCII
            else:
                width = scalar_length
                kind = SourceUnitKind.UNICODE
            self._offset += width
            self._column += 1

        end = self.position
        source_bytes = self._source[start.byte_offset : end.byte_offset]
        return SourceUnit(kind, source_bytes, PositionRange(start, end))


def _utf8_scalar_length(source: bytes, offset: int) -> int | None:
    """Validate exactly one UTF-8 scalar without decoding the complete source."""

    if offset < 0 or offset >= len(source):
        return None

    first = source[offset]
    remaining = len(source) - offset

    if first <= 0x7F:
        return 1

    if 0xC2 <= first <= 0xDF:
        if remaining >= 2 and _is_continuation(source[offset + 1]):
            return 2
        return None

    if 0xE0 <= first <= 0xEF:
        if remaining < 3:
            return None
        second = source[offset + 1]
        third = source[offset + 2]
        second_is_valid = (
            0xA0 <= second <= 0xBF
            if first == 0xE0
            else 0x80 <= second <= 0x9F
            if first == 0xED
            else _is_continuation(second)
        )
        if second_is_valid and _is_continuation(third):
            return 3
        return None

    if 0xF0 <= first <= 0xF4:
        if remaining < 4:
            return None
        second = source[offset + 1]
        third = source[offset + 2]
        fourth = source[offset + 3]
        second_is_valid = (
            0x90 <= second <= 0xBF
            if first == 0xF0
            else 0x80 <= second <= 0x8F
            if first == 0xF4
            else _is_continuation(second)
        )
        if (
            second_is_valid
            and _is_continuation(third)
            and _is_continuation(fourth)
        ):
            return 4
        return None

    return None


def _is_continuation(value: int) -> bool:
    return 0x80 <= value <= 0xBF
