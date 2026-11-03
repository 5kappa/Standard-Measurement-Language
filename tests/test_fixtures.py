import json
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

    def test_out_of_bounds_non_eof_token_is_rejected(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            fixture_root = self._write_pilot_copy(Path(temporary_directory))
            pilot_path = fixture_root / "lexer" / "pilot.json"
            pilot = json.loads(pilot_path.read_text(encoding="utf-8"))
            number = pilot["fixtures"][0]["expected"]["lex"]["tokens"][0]
            number["span"] = {"start_byte": 3, "end_byte": 5}
            pilot_path.write_text(json.dumps(pilot), encoding="utf-8")

            with self.assertRaisesRegex(FixtureFormatError, "exceeds the source"):
                load_lexer_success_fixtures(fixture_root, "lexer/pilot.json")

    def test_token_lexeme_must_match_its_source_slice(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            fixture_root = self._write_pilot_copy(Path(temporary_directory))
            pilot_path = fixture_root / "lexer" / "pilot.json"
            pilot = json.loads(pilot_path.read_text(encoding="utf-8"))
            number = pilot["fixtures"][0]["expected"]["lex"]["tokens"][0]
            number["lexeme"] = "99"
            pilot_path.write_text(json.dumps(pilot), encoding="utf-8")

            with self.assertRaisesRegex(FixtureFormatError, "does not match"):
                load_lexer_success_fixtures(fixture_root, "lexer/pilot.json")

    def _write_pilot_copy(self, fixture_root: Path) -> Path:
        lexer_directory = fixture_root / "lexer"
        lexer_directory.mkdir(parents=True)
        (fixture_root / "index.json").write_bytes(
            (FIXTURE_ROOT / "index.json").read_bytes()
        )
        (lexer_directory / "pilot.json").write_bytes(
            (FIXTURE_ROOT / "lexer" / "pilot.json").read_bytes()
        )
        return fixture_root


if __name__ == "__main__":
    unittest.main()
