from dataclasses import FrozenInstanceError
import unittest

from sml_frontend.diagnostic import (
    Diagnostic,
    DiagnosticCode,
    DiagnosticLabel,
    LabelRole,
)
from sml_frontend.lexer import LexFailure, LexSuccess, _Scanner, lex
from sml_frontend.source import PositionRange, SourcePosition, SourceSpan
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

    def test_unclosed_string_and_block_comment_remain_deferred_to_r8(self) -> None:
        for source in (b'"unclosed', b"/*unclosed"):
            with self.subTest(source=source):
                with self.assertRaisesRegex(NotImplementedError, "R8"):
                    lex(source)

    def test_lone_logical_operators_remain_deferred_to_r9(self) -> None:
        for source in (b"&", b"|"):
            with self.subTest(source=source):
                with self.assertRaisesRegex(NotImplementedError, "R9"):
                    lex(source)


class NumericCandidateTests(unittest.TestCase):
    def test_malformed_candidates_own_their_complete_ranges(self) -> None:
        cases = (
            (b"0123x", DiagnosticCode.LEX003, "0123", "x"),
            (b".5x", DiagnosticCode.LEX004, ".5", "x"),
            (b"5.x", DiagnosticCode.LEX004, "5.", "x"),
            (b"5..2x", DiagnosticCode.LEX004, "5..2", "x"),
            (b"1__0x", DiagnosticCode.LEX005, "1__0", "x"),
            (b"2.5e3foo", DiagnosticCode.LEX006, "2.5e3", "foo"),
            (b"3e+", DiagnosticCode.LEX006, "3e+", None),
            (b"0xGz", DiagnosticCode.LEX007, "0xG", "z"),
            (b"0b1010", DiagnosticCode.LEX007, "0b1010", None),
        )

        for source, code, candidate, later_ident in cases:
            with self.subTest(source=source):
                result = lex(source)

                self.assertIsInstance(result, LexFailure)
                diagnostic = result.diagnostics[0]
                candidate_end = len(candidate.encode("ascii"))
                self.assertEqual(diagnostic.code, code)
                self.assertEqual(
                    diagnostic.primary.span,
                    SourceSpan(0, candidate_end),
                )
                self.assertEqual(
                    diagnostic.data,
                    {"candidate_lexeme": candidate},
                )
                expected_partial_kinds = (
                    [TokenKind.IDENT, TokenKind.EOF]
                    if later_ident is not None
                    else [TokenKind.EOF]
                )
                self.assertEqual(
                    [token.kind for token in result.partial_tokens],
                    expected_partial_kinds,
                )
                if later_ident is not None:
                    self.assertEqual(result.partial_tokens[0].lexeme, later_ident)

    def test_contract_numeric_spelling_variants_are_classified(self) -> None:
        cases = (
            (b"01.5", DiagnosticCode.LEX003),
            (b"1E6", DiagnosticCode.LEX006),
            (b"3e-2", DiagnosticCode.LEX006),
            (b"4E+9", DiagnosticCode.LEX006),
            (b"0XFF", DiagnosticCode.LEX007),
            (b"0B11", DiagnosticCode.LEX007),
        )

        for source, code in cases:
            with self.subTest(source=source):
                result = lex(source)

                self.assertIsInstance(result, LexFailure)
                self.assertEqual(result.diagnostics[0].code, code)
                self.assertEqual(
                    result.diagnostics[0].data,
                    {"candidate_lexeme": source.decode("ascii")},
                )
                self.assertEqual(
                    result.partial_tokens,
                    (Token(TokenKind.EOF, "", SourceSpan(len(source), len(source))),),
                )

    def test_ordinary_attached_e_remains_number_then_identifier(self) -> None:
        result = lex(b"5e")

        self.assertEqual(
            result,
            LexSuccess(
                (
                    Token(TokenKind.NUMBER, "5", SourceSpan(0, 1)),
                    Token(TokenKind.IDENT, "e", SourceSpan(1, 2)),
                    Token(TokenKind.EOF, "", SourceSpan(2, 2)),
                )
            ),
        )

    def test_comma_is_never_absorbed_into_numeric_candidates(self) -> None:
        result = lex(b"1,2")

        self.assertIsInstance(result, LexSuccess)
        self.assertEqual(
            [token.kind for token in result.tokens],
            [TokenKind.NUMBER, TokenKind.COMMA, TokenKind.NUMBER, TokenKind.EOF],
        )


class InvalidUtf8Tests(unittest.TestCase):
    def test_invalid_byte_owns_one_byte_and_scanning_continues(self) -> None:
        result = lex(b"x\xffy")

        self.assertIsInstance(result, LexFailure)
        self.assertEqual(
            result.partial_tokens,
            (
                Token(TokenKind.IDENT, "x", SourceSpan(0, 1)),
                Token(TokenKind.IDENT, "y", SourceSpan(2, 3)),
                Token(TokenKind.EOF, "", SourceSpan(3, 3)),
            ),
        )
        self.assertEqual(len(result.diagnostics), 1)
        diagnostic = result.diagnostics[0]
        self.assertEqual(diagnostic.code, DiagnosticCode.LEX001)
        self.assertEqual(diagnostic.primary.span, SourceSpan(1, 2))
        self.assertEqual(
            diagnostic.primary.positions,
            PositionRange(
                SourcePosition(1, 1, 2),
                SourcePosition(2, 1, 3),
            ),
        )
        self.assertEqual(diagnostic.data, {"invalid_bytes": "ff"})

    def test_bad_bytes_preserve_string_and_comment_states(self) -> None:
        result = lex(b'"a\xffb" c//\xfe\nd/*\xfd*/e')

        self.assertIsInstance(result, LexFailure)
        self.assertEqual(
            [(token.kind, token.lexeme) for token in result.partial_tokens],
            [
                (TokenKind.IDENT, "c"),
                (TokenKind.IDENT, "d"),
                (TokenKind.IDENT, "e"),
                (TokenKind.EOF, ""),
            ],
        )
        self.assertEqual(
            [diagnostic.code for diagnostic in result.diagnostics],
            [DiagnosticCode.LEX001] * 3,
        )
        self.assertEqual(
            [diagnostic.data for diagnostic in result.diagnostics],
            [
                {"invalid_bytes": "ff"},
                {"invalid_bytes": "fe"},
                {"invalid_bytes": "fd"},
            ],
        )


class InvalidSourceCharacterTests(unittest.TestCase):
    def test_complete_unicode_scalar_owns_all_bytes_and_one_column(self) -> None:
        result = lex("xéy".encode("utf-8"))

        self.assertIsInstance(result, LexFailure)
        diagnostic = result.diagnostics[0]
        self.assertEqual(diagnostic.code, DiagnosticCode.LEX002)
        self.assertEqual(diagnostic.primary.span, SourceSpan(1, 3))
        self.assertEqual(
            diagnostic.primary.positions,
            PositionRange(
                SourcePosition(1, 1, 2),
                SourcePosition(3, 1, 3),
            ),
        )
        self.assertEqual(diagnostic.data, {"character_bytes": "c3a9"})

    def test_closed_string_with_failure_emits_no_string_token(self) -> None:
        result = lex(b'"x\\y"')

        self.assertIsInstance(result, LexFailure)
        self.assertEqual(
            result.partial_tokens,
            (Token(TokenKind.EOF, "", SourceSpan(5, 5)),),
        )
        self.assertEqual(result.diagnostics[0].code, DiagnosticCode.LEX002)


if __name__ == "__main__":
    unittest.main()
