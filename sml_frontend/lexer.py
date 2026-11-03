"""Lexer result records and the scanner foundation."""

from __future__ import annotations

from dataclasses import dataclass, field

from .diagnostic import Diagnostic
from .source import SourceCursor, SourceUnit
from .source import SourceSpan
from .token import Token, TokenKind


_RESERVED_IDENTIFIER_KINDS = {
    b"let": TokenKind.LET,
    b"const": TokenKind.CONST,
    b"fn": TokenKind.FN,
    b"return": TokenKind.RETURN,
    b"if": TokenKind.IF,
    b"else": TokenKind.ELSE,
    b"for": TokenKind.FOR,
    b"while": TokenKind.WHILE,
    b"break": TokenKind.BREAK,
    b"continue": TokenKind.CONTINUE,
    b"print": TokenKind.PRINT,
    b"input": TokenKind.INPUT,
    b"assert": TokenKind.ASSERT,
    b"as": TokenKind.AS,
    b"int": TokenKind.INT,
    b"float": TokenKind.FLOAT,
    b"bool": TokenKind.BOOL,
    b"text": TokenKind.TEXT,
    b"Length": TokenKind.LENGTH,
    b"Mass": TokenKind.MASS,
    b"Time": TokenKind.TIME,
    b"Force": TokenKind.FORCE,
    b"to": TokenKind.TO,
    b"then": TokenKind.THEN,
    b"do": TokenKind.DO,
    b"true": TokenKind.TRUE,
    b"false": TokenKind.FALSE,
}

_TWO_BYTE_OPERATOR_KINDS = {
    b"++": TokenKind.PLUS_PLUS,
    b"--": TokenKind.MINUS_MINUS,
    b"+=": TokenKind.PLUS_ASSIGN,
    b"-=": TokenKind.MINUS_ASSIGN,
    b"*=": TokenKind.STAR_ASSIGN,
    b"/=": TokenKind.SLASH_ASSIGN,
    b"<=": TokenKind.LESS_EQUAL,
    b">=": TokenKind.GREATER_EQUAL,
    b"==": TokenKind.EQUAL_EQUAL,
    b"!=": TokenKind.BANG_EQUAL,
    b"&&": TokenKind.AND_AND,
    b"||": TokenKind.OR_OR,
}

_ONE_BYTE_OPERATOR_KINDS = {
    0x2B: TokenKind.PLUS,
    0x2D: TokenKind.MINUS,
    0x2A: TokenKind.STAR,
    0x2F: TokenKind.SLASH,
    0x25: TokenKind.PERCENT,
    0x5E: TokenKind.CARET,
    0x21: TokenKind.BANG,
    0x3D: TokenKind.ASSIGN,
    0x3C: TokenKind.LESS,
    0x3E: TokenKind.GREATER,
}

_DELIMITER_KINDS = {
    0x28: TokenKind.LPAREN,
    0x29: TokenKind.RPAREN,
    0x7B: TokenKind.LBRACE,
    0x7D: TokenKind.RBRACE,
    0x5B: TokenKind.LBRACKET,
    0x5D: TokenKind.RBRACKET,
    0x3B: TokenKind.SEMICOLON,
    0x3A: TokenKind.COLON,
    0x2C: TokenKind.COMMA,
}


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
    """Mutable scan state for the implemented lexer subset."""

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
                self._scan_decimal_number()
            elif byte is not None and _is_ascii_letter(byte):
                self._scan_identifier()
            elif byte == 0x22:
                self._scan_closed_ascii_string()
            elif byte == 0x2F:
                self._scan_slash_prefix()
            elif byte in _ONE_BYTE_OPERATOR_KINDS or byte in b"&|":
                self._scan_operator()
            elif byte in _DELIMITER_KINDS:
                self._scan_delimiter()
            elif byte == 0x20:
                self._skip_ascii_spaces()
            else:
                raise NotImplementedError(
                    "the current lexer subset does not recognize this source byte"
                )

        eof_offset = self.cursor.offset
        self.tokens.append(
            Token(TokenKind.EOF, "", SourceSpan(eof_offset, eof_offset))
        )
        return LexSuccess(tuple(self.tokens))

    def _scan_decimal_number(self) -> None:
        start = self.cursor.offset
        while (byte := self.cursor.peek_byte()) is not None and _is_ascii_digit(byte):
            self.advance_one()
        if self.cursor.peek_byte() == 0x2E and (
            (following_byte := self.cursor.peek_byte(1)) is not None
            and _is_ascii_digit(following_byte)
        ):
            self.advance_one()
            while (byte := self.cursor.peek_byte()) is not None and _is_ascii_digit(
                byte
            ):
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
        spelling = self.source[start : self.cursor.offset]
        kind = _RESERVED_IDENTIFIER_KINDS.get(spelling, TokenKind.IDENT)
        self._emit_ascii_token(kind, start)

    def _scan_closed_ascii_string(self) -> None:
        start = self.cursor.offset
        self.advance_one()
        while (byte := self.cursor.peek_byte()) != 0x22:
            if byte is None or byte in b"\r\n":
                raise NotImplementedError("string termination behavior begins in R5")
            if byte == 0x5C or byte < 0x20 or byte > 0x7E:
                raise NotImplementedError(
                    "string character diagnostics begin after R4"
                )
            self.advance_one()
        self.advance_one()
        self._emit_ascii_token(TokenKind.STRING, start)

    def _scan_slash_prefix(self) -> None:
        prefix = self.source[self.cursor.offset : self.cursor.offset + 2]
        if prefix in (b"//", b"/*"):
            raise NotImplementedError("comment bodies and trivia begin in R5")
        self._scan_operator()

    def _scan_operator(self) -> None:
        start = self.cursor.offset
        spelling = self.source[start : start + 2]
        kind = _TWO_BYTE_OPERATOR_KINDS.get(spelling)
        if kind is not None:
            self.advance_one()
            self.advance_one()
            self._emit_ascii_token(kind, start)
            return

        byte = self.cursor.peek_byte()
        kind = _ONE_BYTE_OPERATOR_KINDS.get(byte)
        if kind is None:
            raise NotImplementedError("lone logical operators begin in R9")
        self.advance_one()
        self._emit_ascii_token(kind, start)

    def _scan_delimiter(self) -> None:
        start = self.cursor.offset
        byte = self.cursor.peek_byte()
        kind = _DELIMITER_KINDS[byte]
        self.advance_one()
        self._emit_ascii_token(kind, start)

    def _skip_ascii_spaces(self) -> None:
        while self.cursor.peek_byte() == 0x20:
            self.advance_one()

    def _reject_deferred_numeric_candidate(self, start: int) -> None:
        spelling = self.source[start : self.cursor.offset]
        integer_spelling = spelling.split(b".", 1)[0]
        next_byte = self.cursor.peek_byte()
        following_byte = self.cursor.peek_byte(1)
        has_leading_zero = len(integer_spelling) > 1 and integer_spelling.startswith(
            b"0"
        )
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
