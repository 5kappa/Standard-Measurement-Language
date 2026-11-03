"""Lexer result records and the scanner foundation."""

from __future__ import annotations

from dataclasses import dataclass, field

from .diagnostic import Diagnostic
from .source import SourceCursor, SourceUnit
from .source import SourceSpan
from .token import Token, TokenKind


_RESERVED_IDENTIFIER_SPELLINGS = frozenset(
    {
        b"let",
        b"const",
        b"fn",
        b"return",
        b"if",
        b"else",
        b"for",
        b"while",
        b"break",
        b"continue",
        b"print",
        b"input",
        b"assert",
        b"as",
        b"int",
        b"float",
        b"bool",
        b"text",
        b"Length",
        b"Mass",
        b"Time",
        b"Force",
        b"to",
        b"then",
        b"do",
        b"true",
        b"false",
    }
)


@dataclass(frozen=True, slots=True)
class LexSuccess:
    tokens: tuple[Token, ...]

    def __post_init__(self) -> None:
        _validate_token_collection(self.tokens)


@dataclass(frozen=True, slots=True)
class LexFailure:
    partial_tokens: tuple[Token, ...]
    diagnostics: tuple[Diagnostic, ...]
    diagnostics_truncated: bool

    def __post_init__(self) -> None:
        _validate_token_collection(self.partial_tokens)
        if not 1 <= len(self.diagnostics) <= 20:
            raise ValueError("LexFailure requires from one through twenty diagnostics")


LexResult = LexSuccess | LexFailure


def lex(source: bytes) -> LexResult:
    """Scan original source bytes using the currently implemented token subset."""

    return _Scanner(source).scan()


def _validate_token_collection(tokens: tuple[Token, ...]) -> None:
    if not tokens or tokens[-1].kind is not TokenKind.EOF:
        raise ValueError("a lexer token collection must end with physical EOF")
    if any(token.kind is TokenKind.EOF for token in tokens[:-1]):
        raise ValueError("a lexer token collection must contain exactly one EOF")


@dataclass(slots=True)
class _Scanner:
    """Mutable scan state for the R2 NUMBER/IDENT/EOF pilot subset."""

    source: bytes
    cursor: SourceCursor = field(init=False)
    tokens: list[Token] = field(default_factory=list, init=False)
    diagnostics: list[Diagnostic] = field(default_factory=list, init=False)
    diagnostics_truncated: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        self.cursor = SourceCursor(self.source)

    def scan(self) -> LexResult:
        while not self.cursor.at_end:
            byte = self.cursor.peek_byte()
            if byte is not None and _is_ascii_digit(byte):
                self._scan_decimal_integer()
            elif byte is not None and _is_ascii_letter(byte):
                self._scan_identifier()
            else:
                raise NotImplementedError(
                    "R2 recognizes only decimal integers and ASCII identifiers"
                )

        eof_offset = self.cursor.offset
        self.tokens.append(
            Token(TokenKind.EOF, "", SourceSpan(eof_offset, eof_offset))
        )
        return LexSuccess(tuple(self.tokens))

    def _scan_decimal_integer(self) -> None:
        start = self.cursor.offset
        while (byte := self.cursor.peek_byte()) is not None and _is_ascii_digit(byte):
            self.advance_one()
        self._reject_deferred_numeric_candidate(start)
        self._emit_ascii_token(TokenKind.NUMBER, start)

    def _scan_identifier(self) -> None:
        start = self.cursor.offset
        self.advance_one()
        while (byte := self.cursor.peek_byte()) is not None and (
            _is_ascii_letter(byte) or _is_ascii_digit(byte) or byte == 0x5F
        ):
            self.advance_one()
        if self.source[start : self.cursor.offset] in _RESERVED_IDENTIFIER_SPELLINGS:
            raise NotImplementedError("reserved-word classification begins in R3/R4")
        self._emit_ascii_token(TokenKind.IDENT, start)

    def _reject_deferred_numeric_candidate(self, start: int) -> None:
        spelling = self.source[start : self.cursor.offset]
        next_byte = self.cursor.peek_byte()
        following_byte = self.cursor.peek_byte(1)
        has_leading_zero = len(spelling) > 1 and spelling.startswith(b"0")
        has_base_prefix = (
            spelling == b"0" and next_byte is not None and next_byte in b"xXbB"
        )
        has_exponent_prefix = next_byte is not None and next_byte in b"eE" and (
            following_byte is not None
            and (_is_ascii_digit(following_byte) or following_byte in b"+-")
        )
        if (
            has_leading_zero
            or has_base_prefix
            or has_exponent_prefix
            or next_byte in (0x2E, 0x5F)
        ):
            raise NotImplementedError("malformed numeric candidates begin in R7")

    def _emit_ascii_token(self, kind: TokenKind, start: int) -> None:
        end = self.cursor.offset
        lexeme = self.source[start:end].decode("ascii")
        self.tokens.append(Token(kind, lexeme, SourceSpan(start, end)))

    def advance_one(self) -> SourceUnit:
        before = self.cursor.offset
        unit = self.cursor.advance()
        self._assert_progress(before)
        return unit

    def _assert_progress(self, before: int) -> None:
        if self.cursor.offset <= before:
            raise RuntimeError("scanner path failed to consume source bytes")


def _is_ascii_digit(value: int) -> bool:
    return 0x30 <= value <= 0x39


def _is_ascii_letter(value: int) -> bool:
    return 0x41 <= value <= 0x5A or 0x61 <= value <= 0x7A
