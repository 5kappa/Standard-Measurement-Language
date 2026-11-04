from dataclasses import FrozenInstanceError
import unittest

from sml_frontend.diagnostic import (
    Diagnostic,
    DiagnosticCode,
    DiagnosticLabel,
    LabelRole,
)
from sml_frontend.lexer import LexFailure, LexSuccess, _Scanner, lex
from sml_frontend.source import SourceSpan
from sml_frontend.token import Token, TokenKind


class SourceFoundationTests(unittest.TestCase):
    def test_success_result_and_tokens_are_immutable(self) -> None:
        eof = Token(TokenKind.EOF, "", SourceSpan(0, 0))
        result = LexSuccess((eof,))

        with self.assertRaises(FrozenInstanceError):
            result.tokens = ()  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            eof.lexeme = "changed"  # type: ignore[misc]

    def test_result_requires_exactly_one_final_eof(self) -> None:
        number = Token(TokenKind.NUMBER, "1", SourceSpan(0, 1))
        eof = Token(TokenKind.EOF, "", SourceSpan(1, 1))

        with self.assertRaises(ValueError):
            LexSuccess((number,))
        with self.assertRaises(ValueError):
            LexSuccess((eof, eof))

    def test_token_lexeme_bytes_must_fill_its_span(self) -> None:
        with self.assertRaises(ValueError):
            Token(TokenKind.IDENT, "name", SourceSpan(0, 3))

    def test_failure_requires_one_through_twenty_diagnostics(self) -> None:
        primary = DiagnosticLabel(LabelRole.PRIMARY, SourceSpan(0, 1))
        diagnostic = Diagnostic(
            DiagnosticCode.LEX002,
            primary,
        )
        eof = Token(TokenKind.EOF, "", SourceSpan(1, 1))

        result = LexFailure((eof,), (diagnostic,), False)

        self.assertEqual(diagnostic.data, {})
        self.assertEqual(result.diagnostics, (diagnostic,))
        with self.assertRaises(ValueError):
            LexFailure((eof,), (), False)
        with self.assertRaises(ValueError):
            LexFailure((eof,), (diagnostic,) * 21, True)

    def test_diagnostic_requires_a_primary_label(self) -> None:
        secondary = DiagnosticLabel(LabelRole.REACHED_EOF, SourceSpan(0, 0))

        with self.assertRaises(ValueError):
            Diagnostic(DiagnosticCode.LEX008, secondary)

    def test_diagnostic_notes_are_empty_in_version_0_1(self) -> None:
        primary = DiagnosticLabel(LabelRole.PRIMARY, SourceSpan(0, 0))
        diagnostic = Diagnostic(DiagnosticCode.LEX008, primary)

        self.assertEqual(diagnostic.notes, ())
        with self.assertRaises(ValueError):
            Diagnostic(
                DiagnosticCode.LEX008,
                primary,
                notes=((),),
            )

    def test_scanner_advance_makes_progress(self) -> None:
        scanner = _Scanner(b"\xff")

        unit = scanner.advance_one()

        self.assertEqual(unit.span, SourceSpan(0, 1))
        self.assertEqual(scanner.cursor.offset, 1)

    def test_scanner_progress_assertion_detects_internal_defect(self) -> None:
        scanner = _Scanner(b"x")

        with self.assertRaises(RuntimeError):
            scanner._assert_progress(scanner.cursor.offset)


class PilotScannerTests(unittest.TestCase):
    def test_token_kind_inventory_contains_exactly_62_kinds(self) -> None:
        self.assertEqual(len(TokenKind), 62)

    def test_attached_quantity_produces_adjacent_tokens_and_eof(self) -> None:
        result = lex(b"10m")

        self.assertEqual(
            result,
            LexSuccess(
                (
                    Token(TokenKind.NUMBER, "10", SourceSpan(0, 2)),
                    Token(TokenKind.IDENT, "m", SourceSpan(2, 3)),
                    Token(TokenKind.EOF, "", SourceSpan(3, 3)),
                )
            ),
        )

    def test_space_gap_preserves_nonadjacent_token_spans(self) -> None:
        result = lex(b"10 foo")

        self.assertEqual(
            result,
            LexSuccess(
                (
                    Token(TokenKind.NUMBER, "10", SourceSpan(0, 2)),
                    Token(TokenKind.IDENT, "foo", SourceSpan(3, 6)),
                    Token(TokenKind.EOF, "", SourceSpan(6, 6)),
                )
            ),
        )

    def test_complete_identifier_is_classified_by_exact_reserved_spelling(self) -> None:
        cases = {
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

        for spelling, expected_kind in cases.items():
            with self.subTest(spelling=spelling):
                result = lex(spelling)
                self.assertIsInstance(result, LexSuccess)
                self.assertEqual(result.tokens[0].kind, expected_kind)
                self.assertEqual(result.tokens[0].lexeme, spelling.decode("ascii"))

    def test_longest_valid_operator_wins(self) -> None:
        cases = {
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

        for spelling, expected_kind in cases.items():
            with self.subTest(spelling=spelling):
                result = lex(spelling)
                self.assertIsInstance(result, LexSuccess)
                self.assertEqual(result.tokens[0].kind, expected_kind)
                self.assertEqual(result.tokens[0].lexeme, spelling.decode("ascii"))

    def test_single_byte_operators_and_delimiters_are_tokens(self) -> None:
        cases = {
            b"+": TokenKind.PLUS,
            b"-": TokenKind.MINUS,
            b"*": TokenKind.STAR,
            b"/": TokenKind.SLASH,
            b"%": TokenKind.PERCENT,
            b"^": TokenKind.CARET,
            b"!": TokenKind.BANG,
            b"=": TokenKind.ASSIGN,
            b"<": TokenKind.LESS,
            b">": TokenKind.GREATER,
            b"(": TokenKind.LPAREN,
            b")": TokenKind.RPAREN,
            b"{": TokenKind.LBRACE,
            b"}": TokenKind.RBRACE,
            b"[": TokenKind.LBRACKET,
            b"]": TokenKind.RBRACKET,
            b";": TokenKind.SEMICOLON,
            b":": TokenKind.COLON,
            b",": TokenKind.COMMA,
        }

        for spelling, expected_kind in cases.items():
            with self.subTest(spelling=spelling):
                result = lex(spelling)
                self.assertIsInstance(result, LexSuccess)
                self.assertEqual(result.tokens[0].kind, expected_kind)

    def test_comments_are_skipped_and_leave_physical_span_gaps(self) -> None:
        result = lex(b"10/*note*/m 20//line\r\nkg")

        self.assertEqual(
            result,
            LexSuccess(
                (
                    Token(TokenKind.NUMBER, "10", SourceSpan(0, 2)),
                    Token(TokenKind.IDENT, "m", SourceSpan(10, 11)),
                    Token(TokenKind.NUMBER, "20", SourceSpan(12, 14)),
                    Token(TokenKind.IDENT, "kg", SourceSpan(22, 24)),
                    Token(TokenKind.EOF, "", SourceSpan(24, 24)),
                )
            ),
        )

    def test_block_comment_closes_at_first_terminator_without_nesting(self) -> None:
        result = lex(b"/* outer /* inner */ x")

        self.assertEqual(
            result,
            LexSuccess(
                (
                    Token(TokenKind.IDENT, "x", SourceSpan(21, 22)),
                    Token(TokenKind.EOF, "", SourceSpan(22, 22)),
                )
            ),
        )

    def test_lf_cr_crlf_and_tabs_are_skipped_as_trivia(self) -> None:
        result = lex(b"a\nb\rc\r\n\td\te")

        self.assertEqual(
            [token.span for token in result.tokens],
            [
                SourceSpan(0, 1),
                SourceSpan(2, 3),
                SourceSpan(4, 5),
                SourceSpan(8, 9),
                SourceSpan(10, 11),
                SourceSpan(11, 11),
            ],
        )

    def test_trailing_whitespace_reaches_physical_eof(self) -> None:
        result = lex(b"x \t\r\n")

        self.assertEqual(
            result,
            LexSuccess(
                (
                    Token(TokenKind.IDENT, "x", SourceSpan(0, 1)),
                    Token(TokenKind.EOF, "", SourceSpan(5, 5)),
                )
            ),
        )

    def test_closed_ascii_string_is_constructible_for_the_r4_inventory(self) -> None:
        result = lex(b'"x"')

        self.assertEqual(
            result,
            LexSuccess(
                (
                    Token(TokenKind.STRING, '"x"', SourceSpan(0, 3)),
                    Token(TokenKind.EOF, "", SourceSpan(3, 3)),
                )
            ),
        )

    def test_invalid_string_and_comment_characters_remain_deferred_to_r6(self) -> None:
        for source in (b'"bad\\character"', b"//bad\\character"):
            with self.subTest(source=source):
                with self.assertRaisesRegex(NotImplementedError, "R6"):
                    lex(source)

    def test_unclosed_string_and_block_comment_remain_deferred_to_r8(self) -> None:
        for source in (b'"unclosed', b"/*unclosed"):
            with self.subTest(source=source):
                with self.assertRaisesRegex(NotImplementedError, "R8"):
                    lex(source)

    def test_unimplemented_surface_fails_loudly(self) -> None:
        deferred_sources = (b"0123", b"2.5e3", b"0x10")

        for source in deferred_sources:
            with self.subTest(source=source):
                with self.assertRaises(NotImplementedError):
                    lex(source)


if __name__ == "__main__":
    unittest.main()
