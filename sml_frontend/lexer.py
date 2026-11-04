"""Lexer result records and the scanner foundation."""

from __future__ import annotations

from dataclasses import dataclass, field

from .diagnostic import Diagnostic, DiagnosticCode, DiagnosticLabel, LabelRole
from .source import (
    PositionRange,
    SourceCursor,
    SourcePosition,
    SourceSpan,
    SourceUnit,
    SourceUnitKind,
)
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

_CANONICAL_SYMBOL_BYTES = b".+-*/%^<>=!&|(){}[];:,\"_"
_WHITESPACE_BYTES = b" \t\r\n"
_DIAGNOSTIC_LIMIT = 20


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
            if self.cursor.utf8_scalar_length() is None:
                self._report_invalid_utf8_byte()
            elif byte is not None and byte >= 0x80:
                self._report_invalid_source_character()
            elif byte is not None and _is_ascii_digit(byte):
                self._scan_numeric_candidate()
            elif byte is not None and _is_ascii_letter(byte):
                self._scan_identifier()
            elif byte == 0x22:
                self._scan_string()
            elif byte == 0x2F:
                self._scan_slash_prefix()
            elif byte in _ONE_BYTE_OPERATOR_KINDS or byte in b"&|":
                self._scan_operator()
            elif byte in _DELIMITER_KINDS:
                self._scan_delimiter()
            elif byte in _WHITESPACE_BYTES:
                self._skip_whitespace()
            elif byte == 0x2E:
                self._scan_leading_decimal_candidate()
            else:
                self._report_invalid_source_character()

        eof_offset = self.cursor.offset
        self.tokens.append(
            Token(TokenKind.EOF, "", SourceSpan(eof_offset, eof_offset))
        )
        if self.diagnostics:
            return LexFailure(
                tuple(self.tokens),
                tuple(self.diagnostics),
                self.diagnostics_truncated,
            )
        return LexSuccess(tuple(self.tokens))

    def _scan_numeric_candidate(self) -> None:
        start = self.cursor.offset
        start_position = self.cursor.position
        while (byte := self.cursor.peek_byte()) is not None and _is_ascii_digit(byte):
            self.advance_one()

        integer_end = self.cursor.offset
        integer_spelling = self.source[start:integer_end]
        next_byte = self.cursor.peek_byte()
        if (
            integer_spelling == b"0"
            and next_byte is not None
            and next_byte in b"xXbB"
        ):
            self._scan_alternate_base_candidate(start, start_position)
            return

        dot_count = 0
        while (byte := self.cursor.peek_byte()) is not None and (
            _is_ascii_digit(byte) or byte == 0x2E
        ):
            if byte == 0x2E:
                dot_count += 1
            self.advance_one()

        if self._consume_numeric_separator_continuation():
            self._report_numeric_failure(
                DiagnosticCode.LEX005,
                start,
                start_position,
            )
            return

        has_leading_zero = len(integer_spelling) > 1 and integer_spelling.startswith(
            b"0"
        )
        decimal_spelling = self.source[start : self.cursor.offset]
        has_malformed_decimal = dot_count > 1 or (
            dot_count == 1 and decimal_spelling.endswith(b".")
        )

        next_byte = self.cursor.peek_byte()
        following_byte = self.cursor.peek_byte(1)
        has_exponent_prefix = (
            not has_leading_zero
            and not has_malformed_decimal
            and next_byte is not None
            and next_byte in b"eE"
            and following_byte is not None
            and (_is_ascii_digit(following_byte) or following_byte in b"+-")
        )
        if has_exponent_prefix:
            self.advance_one()
            sign = self.cursor.peek_byte()
            if sign is not None and sign in b"+-":
                self.advance_one()
            while (byte := self.cursor.peek_byte()) is not None and _is_ascii_digit(
                byte
            ):
                self.advance_one()
            self._consume_numeric_separator_continuation()
            self._report_numeric_failure(
                DiagnosticCode.LEX006,
                start,
                start_position,
            )
            return

        if has_leading_zero:
            self._report_numeric_failure(
                DiagnosticCode.LEX003,
                start,
                start_position,
            )
            return
        if has_malformed_decimal:
            self._report_numeric_failure(
                DiagnosticCode.LEX004,
                start,
                start_position,
            )
            return
        self._emit_ascii_token(TokenKind.NUMBER, start)

    def _scan_leading_decimal_candidate(self) -> None:
        start = self.cursor.offset
        start_position = self.cursor.position
        self.advance_one()
        while (byte := self.cursor.peek_byte()) is not None and (
            _is_ascii_digit(byte) or byte == 0x2E
        ):
            self.advance_one()
        if self._consume_numeric_separator_continuation():
            self._report_numeric_failure(
                DiagnosticCode.LEX005,
                start,
                start_position,
            )
            return
        self._report_numeric_failure(
            DiagnosticCode.LEX004,
            start,
            start_position,
        )

    def _scan_alternate_base_candidate(
        self,
        start: int,
        start_position: SourcePosition,
    ) -> None:
        prefix = self.cursor.peek_byte()
        self.advance_one()
        payload_start = self.cursor.offset
        if prefix in b"xX":
            while (byte := self.cursor.peek_byte()) is not None and _is_ascii_hex_digit(
                byte
            ):
                self.advance_one()
        else:
            while (byte := self.cursor.peek_byte()) is not None and _is_ascii_digit(
                byte
            ):
                self.advance_one()

        byte = self.cursor.peek_byte()
        if self.cursor.offset == payload_start and byte is not None and (
            _is_ascii_letter(byte) or _is_ascii_digit(byte)
        ):
            self.advance_one()

        self._consume_numeric_separator_continuation(
            hexadecimal=prefix in b"xX",
        )
        self._report_numeric_failure(
            DiagnosticCode.LEX007,
            start,
            start_position,
        )

    def _consume_numeric_separator_continuation(
        self,
        *,
        hexadecimal: bool = False,
    ) -> bool:
        if self.cursor.peek_byte() != 0x5F:
            return False
        while (byte := self.cursor.peek_byte()) is not None:
            is_digit = (
                _is_ascii_hex_digit(byte) if hexadecimal else _is_ascii_digit(byte)
            )
            if not is_digit and byte not in b"._":
                break
            self.advance_one()
        return True

    def _report_numeric_failure(
        self,
        code: DiagnosticCode,
        start: int,
        start_position: SourcePosition,
    ) -> None:
        end = self.cursor.offset
        self._record_diagnostic(
            Diagnostic(
                code,
                DiagnosticLabel(
                    LabelRole.PRIMARY,
                    SourceSpan(start, end),
                    PositionRange(start_position, self.cursor.position),
                ),
                data={"candidate_lexeme": self.source[start:end].decode("ascii")},
            )
        )

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

    def _scan_string(self) -> None:
        start = self.cursor.offset
        start_position = self.cursor.position
        had_lexical_failure = False
        self.advance_one()
        while (byte := self.cursor.peek_byte()) != 0x22:
            if byte is None or byte in b"\r\n":
                if byte is None:
                    termination = "EOF"
                elif byte == 0x0A:
                    termination = "LF"
                elif self.cursor.peek_byte(1) == 0x0A:
                    termination = "CRLF"
                else:
                    termination = "CR"
                self._record_diagnostic(
                    Diagnostic(
                        DiagnosticCode.LEX008,
                        DiagnosticLabel(
                            LabelRole.PRIMARY,
                            SourceSpan(start, self.cursor.offset),
                            PositionRange(start_position, self.cursor.position),
                        ),
                        data={"termination": termination},
                    ),
                )
                return
            if self.cursor.utf8_scalar_length() is None:
                self._report_invalid_utf8_byte()
                had_lexical_failure = True
            elif byte >= 0x80 or not _is_canonical_ascii(byte):
                self._report_invalid_source_character()
                had_lexical_failure = True
            else:
                self.advance_one()
        self.advance_one()
        if not had_lexical_failure:
            self._emit_ascii_token(TokenKind.STRING, start)

    def _scan_slash_prefix(self) -> None:
        prefix = self.source[self.cursor.offset : self.cursor.offset + 2]
        if prefix == b"//":
            self._skip_line_comment()
            return
        if prefix == b"/*":
            self._skip_block_comment()
            return
        self._scan_operator()

    def _skip_line_comment(self) -> None:
        self.advance_one()
        self.advance_one()
        while (byte := self.cursor.peek_byte()) is not None and byte not in b"\r\n":
            self._advance_comment_content()

    def _skip_block_comment(self) -> None:
        start = self.cursor.offset
        start_position = self.cursor.position
        self.advance_one()
        self.advance_one()
        opener_end_position = self.cursor.position
        while not self.cursor.at_end:
            if self.source[self.cursor.offset : self.cursor.offset + 2] == b"*/":
                self.advance_one()
                self.advance_one()
                return
            self._advance_comment_content()
        eof_offset = self.cursor.offset
        eof_position = self.cursor.position
        self._record_diagnostic(
            Diagnostic(
                DiagnosticCode.LEX009,
                DiagnosticLabel(
                    LabelRole.PRIMARY,
                    SourceSpan(start, start + 2),
                    PositionRange(start_position, opener_end_position),
                ),
                secondary=(
                    DiagnosticLabel(
                        LabelRole.REACHED_EOF,
                        SourceSpan(eof_offset, eof_offset),
                        PositionRange(eof_position, eof_position),
                    ),
                ),
            ),
        )

    def _advance_comment_content(self) -> None:
        byte = self.cursor.peek_byte()
        if byte is None:
            raise RuntimeError("comment content cannot advance beyond EOF")
        if self.cursor.utf8_scalar_length() is None:
            self._report_invalid_utf8_byte()
        elif byte >= 0x80 or not _is_canonical_ascii(byte):
            self._report_invalid_source_character()
        else:
            self.advance_one()

    def _report_invalid_utf8_byte(self) -> None:
        unit = self.advance_one()
        if unit.kind is not SourceUnitKind.INVALID_UTF8:
            raise RuntimeError("LEX001 must consume exactly one invalid UTF-8 byte")
        self._record_diagnostic(
            Diagnostic(
                DiagnosticCode.LEX001,
                DiagnosticLabel(
                    LabelRole.PRIMARY,
                    unit.span,
                    unit.positions,
                ),
                data={"invalid_bytes": unit.source_bytes.hex()},
            )
        )

    def _report_invalid_source_character(self) -> None:
        unit = self.advance_one()
        if unit.kind is SourceUnitKind.INVALID_UTF8:
            raise RuntimeError("LEX002 requires a complete well-formed UTF-8 scalar")
        self._record_diagnostic(
            Diagnostic(
                DiagnosticCode.LEX002,
                DiagnosticLabel(
                    LabelRole.PRIMARY,
                    unit.span,
                    unit.positions,
                ),
                data={"character_bytes": unit.source_bytes.hex()},
            )
        )

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
            unit = self.advance_one()
            self._record_diagnostic(
                Diagnostic(
                    DiagnosticCode.LEX010,
                    DiagnosticLabel(
                        LabelRole.PRIMARY,
                        unit.span,
                        unit.positions,
                    ),
                    data={"operator_lexeme": unit.source_bytes.decode("ascii")},
                )
            )
            return
        self.advance_one()
        self._emit_ascii_token(kind, start)

    def _record_diagnostic(self, diagnostic: Diagnostic) -> None:
        key = _diagnostic_sort_key(diagnostic)
        if len(self.diagnostics) < _DIAGNOSTIC_LIMIT:
            self.diagnostics.append(diagnostic)
            self.diagnostics.sort(key=_diagnostic_sort_key)
            return

        self.diagnostics_truncated = True
        if key < _diagnostic_sort_key(self.diagnostics[-1]):
            self.diagnostics[-1] = diagnostic
            self.diagnostics.sort(key=_diagnostic_sort_key)

    def _scan_delimiter(self) -> None:
        start = self.cursor.offset
        byte = self.cursor.peek_byte()
        kind = _DELIMITER_KINDS[byte]
        self.advance_one()
        self._emit_ascii_token(kind, start)

    def _skip_whitespace(self) -> None:
        while (
            (byte := self.cursor.peek_byte()) is not None
            and byte in _WHITESPACE_BYTES
        ):
            self.advance_one()

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


def _is_ascii_hex_digit(value: int) -> bool:
    return (
        _is_ascii_digit(value)
        or 0x41 <= value <= 0x46
        or 0x61 <= value <= 0x66
    )


def _is_canonical_ascii(value: int) -> bool:
    return (
        _is_ascii_letter(value)
        or _is_ascii_digit(value)
        or value in _WHITESPACE_BYTES
        or value in _CANONICAL_SYMBOL_BYTES
    )


def _diagnostic_sort_key(diagnostic: Diagnostic) -> tuple[int, int, str]:
    span = diagnostic.primary.span
    return span.start_byte, span.end_byte, diagnostic.code.value
