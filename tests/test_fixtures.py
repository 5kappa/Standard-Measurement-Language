from pathlib import Path
import unittest

from sml_frontend.lexer import lex
from tests.fixture_loader import load_lexer_success_fixtures


FIXTURE_ROOT = Path(__file__).parents[1] / "docs" / "frontend" / "fixtures"


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


if __name__ == "__main__":
    unittest.main()
