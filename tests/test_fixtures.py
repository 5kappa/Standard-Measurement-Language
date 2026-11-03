from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from sml_frontend.fixture_loader import (
    FixtureFormatError,
    load_lexer_success_fixtures,
    load_strict_json,
)
from sml_frontend.lexer import lex


FIXTURE_ROOT = Path(__file__).parents[1] / "docs" / "frontend" / "fixtures"


class PilotLexerFixtureTests(unittest.TestCase):
    def test_authoritative_pilot_fixture(self) -> None:
        fixtures = load_lexer_success_fixtures(FIXTURE_ROOT, "lexer/pilot.json")

        self.assertEqual(
            [fixture.fixture_id for fixture in fixtures],
            ["lex-pilot-attached-quantity-tokens"],
        )
        for fixture in fixtures:
            with self.subTest(fixture=fixture.fixture_id):
                self.assertEqual(lex(fixture.source), fixture.expected)

    def test_unindexed_file_is_rejected(self) -> None:
        with self.assertRaisesRegex(FixtureFormatError, "not indexed"):
            load_lexer_success_fixtures(FIXTURE_ROOT, "lexer/missing.json")

    def test_duplicate_json_keys_are_rejected(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "duplicate.json"
            path.write_text('{"format_version": 1, "format_version": 1}', encoding="utf-8")

            with self.assertRaisesRegex(FixtureFormatError, "duplicate JSON object key"):
                load_strict_json(path)


if __name__ == "__main__":
    unittest.main()
