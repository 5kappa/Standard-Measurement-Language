from pathlib import Path
import unittest

from sml_frontend.lexer import LexSuccess, lex
from tests.fixture_loader import (
    LexerFixture,
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


if __name__ == "__main__":
    unittest.main()
