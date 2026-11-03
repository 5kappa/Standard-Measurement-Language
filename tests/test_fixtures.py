from pathlib import Path
import unittest

from sml_frontend.lexer import lex
from tests.fixture_loader import load_lexer_success_fixtures


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


if __name__ == "__main__":
    unittest.main()
