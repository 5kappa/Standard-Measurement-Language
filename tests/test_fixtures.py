from pathlib import Path
import unittest

from sml_frontend.lexer import LexFailure, LexSuccess, lex
from tests.fixture_loader import (
    LexerFailureFixture,
    LexerFixture,
    load_lexer_failure_fixtures,
    load_lexer_success_fixtures,
    locate_token_positions,
)


FIXTURE_ROOT = Path(__file__).parents[1] / "docs" / "frontend" / "fixtures"


ORDINARY_TOKEN_FIXTURE_IDS = (
    "lex-keyword-near-misses-identifiers",
    "lex-accepted-numbers-and-signs",
    "lex-ordinary-attached-e-identifier",
)

BASIC_LOCATION_FIXTURE_IDS = (
    "location-empty-source",
    "location-adjacent-quantity-boundary",
    "location-space-detached-quantity-boundary",
)

TOKEN_INVENTORY_FIXTURE_IDS = (
    "lex-all-token-kinds",
    "lex-maximal-munch-boundaries",
)

TRIVIA_TOKEN_FIXTURE_IDS = (
    "lex-complete-strings",
    "lex-comments-adjacency-and-nonnesting",
)

TRIVIA_LOCATION_FIXTURE_IDS = (
    "location-comment-detached-quantity-boundary",
    "location-newline-and-tab-forms",
    "location-multiline-block-comment",
)

SOURCE_CHARACTER_LOCATION_FIXTURE_IDS = (
    "location-invalid-unicode-scalar",
)

SOURCE_CHARACTER_LEXER_FIXTURE_IDS = (
    "lex-invalid-leading-underscore",
    "lex-invalid-character-closed-string",
    "lex-invalid-character-line-comment",
    "lex-invalid-character-block-comment",
    "lex-malformed-gap-preserves-spans",
)

SOURCE_CHARACTER_FRONTEND_FIXTURE_IDS = (
    "frontend-pilot-invalid-utf8-phase-gate",
)

MALFORMED_NUMBER_FIXTURE_IDS = (
    "lex-leading-zero",
    "lex-malformed-leading-decimal",
    "lex-malformed-trailing-decimal",
    "lex-malformed-repeated-decimal",
    "lex-numeric-separator",
    "lex-numeric-separator-exact-boundary",
    "lex-scientific-boundary",
    "lex-scientific-notation",
    "lex-scientific-incomplete-sign",
    "lex-alternate-base-empty",
    "lex-hex-notation",
    "lex-hex-boundary",
    "lex-hex-invalid-digit-exact-boundary",
    "lex-binary-notation",
    "lex-repeated-decimal-exact-boundary",
)

STRING_COMMENT_FAILURE_FIXTURE_IDS = (
    "lex-invalid-character-unclosed-string",
    "lex-unclosed-string-lf",
    "lex-unclosed-string-cr",
    "lex-unclosed-string-crlf",
    "lex-unclosed-string-eof",
    "lex-unterminated-block-comment",
)


class PilotLexerFixtureTests(unittest.TestCase):
    def test_authoritative_pilot_fixture(self) -> None:
        fixtures = load_lexer_success_fixtures(FIXTURE_ROOT / "lexer" / "pilot.json")

        self.assertEqual(
            [fixture.fixture_id for fixture in fixtures],
            ["lex-pilot-attached-quantity-tokens"],
        )
        for fixture in fixtures:
            with self.subTest(fixture=fixture.fixture_id):
                self.assertEqual(lex(fixture.source), fixture.expected)


class OrdinaryTokenFixtureTests(unittest.TestCase):
    def test_r3_ordinary_token_fixtures(self) -> None:
        fixtures = load_lexer_success_fixtures(
            FIXTURE_ROOT / "lexer" / "tokens.json",
            ORDINARY_TOKEN_FIXTURE_IDS,
        )

        self.assertEqual(
            [fixture.fixture_id for fixture in fixtures],
            list(ORDINARY_TOKEN_FIXTURE_IDS),
        )
        for fixture in fixtures:
            with self.subTest(fixture=fixture.fixture_id):
                self.assertEqual(lex(fixture.source), fixture.expected)


class BasicLocationFixtureTests(unittest.TestCase):
    def test_r3_basic_location_fixtures(self) -> None:
        fixtures = load_lexer_success_fixtures(
            FIXTURE_ROOT / "locations" / "source-locations.json",
            BASIC_LOCATION_FIXTURE_IDS,
        )

        self.assertEqual(
            [fixture.fixture_id for fixture in fixtures],
            list(BASIC_LOCATION_FIXTURE_IDS),
        )
        for fixture in fixtures:
            with self.subTest(fixture=fixture.fixture_id):
                self.assertEqual(lex(fixture.source), fixture.expected)


class TokenInventoryFixtureTests(unittest.TestCase):
    def test_r4_token_inventory_fixtures(self) -> None:
        fixtures = load_lexer_success_fixtures(
            FIXTURE_ROOT / "lexer" / "tokens.json",
            TOKEN_INVENTORY_FIXTURE_IDS,
        )

        self.assertEqual(
            [fixture.fixture_id for fixture in fixtures],
            list(TOKEN_INVENTORY_FIXTURE_IDS),
        )
        for fixture in fixtures:
            with self.subTest(fixture=fixture.fixture_id):
                self.assertEqual(lex(fixture.source), fixture.expected)


class TriviaAndPositionFixtureTests(unittest.TestCase):
    def test_r5_successful_trivia_and_position_fixtures(self) -> None:
        token_fixtures = load_lexer_success_fixtures(
            FIXTURE_ROOT / "lexer" / "tokens.json",
            TRIVIA_TOKEN_FIXTURE_IDS,
        )
        location_fixtures = load_lexer_success_fixtures(
            FIXTURE_ROOT / "locations" / "source-locations.json",
            TRIVIA_LOCATION_FIXTURE_IDS,
        )
        fixtures = token_fixtures + location_fixtures

        self.assertEqual(
            [fixture.fixture_id for fixture in fixtures],
            list(TRIVIA_TOKEN_FIXTURE_IDS + TRIVIA_LOCATION_FIXTURE_IDS),
        )
        for fixture in fixtures:
            with self.subTest(fixture=fixture.fixture_id):
                self._assert_fixture(fixture)

    def _assert_fixture(self, fixture: LexerFixture) -> None:
        actual = lex(fixture.source)
        self.assertEqual(actual, fixture.expected)
        self.assertIsInstance(actual, LexSuccess)
        actual_positions = locate_token_positions(fixture.source, actual.tokens)
        for index, expected_positions in enumerate(fixture.expected_positions):
            if expected_positions is not None:
                self.assertEqual(actual_positions[index], expected_positions)


class SourceCharacterFixtureTests(unittest.TestCase):
    def test_r6_source_character_fixtures(self) -> None:
        location_fixtures = load_lexer_failure_fixtures(
            FIXTURE_ROOT / "locations" / "source-locations.json",
            SOURCE_CHARACTER_LOCATION_FIXTURE_IDS,
        )
        lexer_fixtures = load_lexer_failure_fixtures(
            FIXTURE_ROOT / "lexer" / "lexical-failures.json",
            SOURCE_CHARACTER_LEXER_FIXTURE_IDS,
        )
        frontend_fixtures = load_lexer_failure_fixtures(
            FIXTURE_ROOT / "frontend" / "pilot.json",
            SOURCE_CHARACTER_FRONTEND_FIXTURE_IDS,
        )
        fixtures = location_fixtures + lexer_fixtures + frontend_fixtures

        self.assertEqual(
            [fixture.fixture_id for fixture in fixtures],
            list(
                SOURCE_CHARACTER_LOCATION_FIXTURE_IDS
                + SOURCE_CHARACTER_LEXER_FIXTURE_IDS
                + SOURCE_CHARACTER_FRONTEND_FIXTURE_IDS
            ),
        )
        for fixture in fixtures:
            with self.subTest(fixture=fixture.fixture_id):
                self._assert_failure_fixture(fixture)

    def test_lexical_failure_keeps_parser_callback_unreachable(self) -> None:
        fixture = load_lexer_failure_fixtures(
            FIXTURE_ROOT / "frontend" / "pilot.json",
            SOURCE_CHARACTER_FRONTEND_FIXTURE_IDS,
        )[0]
        parser_calls = []
        result = lex(fixture.source)

        if isinstance(result, LexSuccess):
            parser_calls.append(result.tokens)

        self.assertIsInstance(result, LexFailure)
        self.assertTrue(fixture.expects_parse_not_run)
        self.assertEqual(parser_calls, [])

    def _assert_failure_fixture(self, fixture: LexerFailureFixture) -> None:
        actual = lex(fixture.source)
        self.assertIsInstance(actual, LexFailure)
        self.assertEqual(actual.partial_tokens, fixture.expected.partial_tokens)
        self.assertEqual(
            actual.diagnostics_truncated,
            fixture.expected.diagnostics_truncated,
        )
        self.assertEqual(len(actual.diagnostics), len(fixture.expected.diagnostics))

        actual_token_positions = locate_token_positions(
            fixture.source,
            actual.partial_tokens,
        )
        for index, expected_positions in enumerate(
            fixture.expected_token_positions
        ):
            if expected_positions is not None:
                self.assertEqual(
                    actual_token_positions[index],
                    expected_positions,
                )

        for actual_diagnostic, expected_diagnostic in zip(
            actual.diagnostics,
            fixture.expected.diagnostics,
            strict=True,
        ):
            self.assertEqual(actual_diagnostic.code, expected_diagnostic.code)
            self.assertEqual(actual_diagnostic.phase, expected_diagnostic.phase)
            self.assertEqual(actual_diagnostic.severity, expected_diagnostic.severity)
            self.assertEqual(actual_diagnostic.notes, expected_diagnostic.notes)
            self.assertEqual(actual_diagnostic.data, expected_diagnostic.data)
            self._assert_label(
                actual_diagnostic.primary,
                expected_diagnostic.primary,
            )
            self.assertEqual(
                len(actual_diagnostic.secondary),
                len(expected_diagnostic.secondary),
            )
            for actual_label, expected_label in zip(
                actual_diagnostic.secondary,
                expected_diagnostic.secondary,
                strict=True,
            ):
                self._assert_label(actual_label, expected_label)

    def _assert_label(self, actual, expected) -> None:
        self.assertEqual(actual.role, expected.role)
        self.assertEqual(actual.span, expected.span)
        if expected.positions is not None:
            self.assertEqual(actual.positions, expected.positions)


class MalformedNumberFixtureTests(unittest.TestCase):
    def test_r7_malformed_number_fixtures(self) -> None:
        fixtures = load_lexer_failure_fixtures(
            FIXTURE_ROOT / "lexer" / "lexical-failures.json",
            MALFORMED_NUMBER_FIXTURE_IDS,
        )

        self.assertEqual(
            [fixture.fixture_id for fixture in fixtures],
            list(MALFORMED_NUMBER_FIXTURE_IDS),
        )
        for fixture in fixtures:
            with self.subTest(fixture=fixture.fixture_id):
                actual = lex(fixture.source)
                self.assertIsInstance(actual, LexFailure)
                self.assertTrue(fixture.expects_parse_not_run)
                self.assertEqual(
                    actual.partial_tokens,
                    fixture.expected.partial_tokens,
                )
                self.assertEqual(
                    actual.diagnostics_truncated,
                    fixture.expected.diagnostics_truncated,
                )
                self.assertEqual(len(actual.diagnostics), 1)
                actual_diagnostic = actual.diagnostics[0]
                expected_diagnostic = fixture.expected.diagnostics[0]
                self.assertEqual(actual_diagnostic.code, expected_diagnostic.code)
                self.assertEqual(
                    actual_diagnostic.primary.span,
                    expected_diagnostic.primary.span,
                )
                self.assertEqual(
                    actual_diagnostic.data,
                    expected_diagnostic.data,
                )


class StringCommentFailureFixtureTests(unittest.TestCase):
    def test_r8_string_and_comment_failure_fixtures(self) -> None:
        fixtures = load_lexer_failure_fixtures(
            FIXTURE_ROOT / "lexer" / "lexical-failures.json",
            STRING_COMMENT_FAILURE_FIXTURE_IDS,
        )

        self.assertEqual(
            [fixture.fixture_id for fixture in fixtures],
            list(STRING_COMMENT_FAILURE_FIXTURE_IDS),
        )
        for fixture in fixtures:
            with self.subTest(fixture=fixture.fixture_id):
                actual = lex(fixture.source)

                self.assertIsInstance(actual, LexFailure)
                self.assertTrue(fixture.expects_parse_not_run)
                self.assertEqual(
                    actual.partial_tokens,
                    fixture.expected.partial_tokens,
                )
                self.assertEqual(
                    actual.diagnostics_truncated,
                    fixture.expected.diagnostics_truncated,
                )
                self.assertEqual(
                    len(actual.diagnostics),
                    len(fixture.expected.diagnostics),
                )

                actual_token_positions = locate_token_positions(
                    fixture.source,
                    actual.partial_tokens,
                )
                for index, expected_positions in enumerate(
                    fixture.expected_token_positions
                ):
                    if expected_positions is not None:
                        self.assertEqual(
                            actual_token_positions[index],
                            expected_positions,
                        )

                for actual_diagnostic, expected_diagnostic in zip(
                    actual.diagnostics,
                    fixture.expected.diagnostics,
                    strict=True,
                ):
                    self.assertEqual(actual_diagnostic.code, expected_diagnostic.code)
                    self.assertEqual(actual_diagnostic.phase, expected_diagnostic.phase)
                    self.assertEqual(
                        actual_diagnostic.severity,
                        expected_diagnostic.severity,
                    )
                    self.assertEqual(actual_diagnostic.notes, expected_diagnostic.notes)
                    self.assertEqual(actual_diagnostic.data, expected_diagnostic.data)
                    self._assert_label(
                        actual_diagnostic.primary,
                        expected_diagnostic.primary,
                    )
                    self.assertEqual(
                        len(actual_diagnostic.secondary),
                        len(expected_diagnostic.secondary),
                    )
                    for actual_label, expected_label in zip(
                        actual_diagnostic.secondary,
                        expected_diagnostic.secondary,
                        strict=True,
                    ):
                        self._assert_label(actual_label, expected_label)

    def _assert_label(self, actual, expected) -> None:
        self.assertEqual(actual.role, expected.role)
        self.assertEqual(actual.span, expected.span)
        if expected.positions is not None:
            self.assertEqual(actual.positions, expected.positions)


if __name__ == "__main__":
    unittest.main()
