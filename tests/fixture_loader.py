"""Read trusted lexer fixtures into the records used by conformance tests."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from sml_frontend.lexer import LexSuccess
from sml_frontend.source import SourceSpan
from sml_frontend.token import Token, TokenKind


@dataclass(frozen=True, slots=True)
class LexerFixture:
    fixture_id: str
    source: bytes
    expected: LexSuccess


def load_lexer_success_fixtures(path: Path) -> tuple[LexerFixture, ...]:
    """Decode the trusted UTF-8 lexer-success fixtures in ``path``."""

    with path.open(encoding="utf-8") as fixture_file:
        document = json.load(fixture_file)

    if document["format_version"] != 1 or document["language_version"] != "0.1":
        raise ValueError("unsupported fixture format or language version")

    fixtures = []
    for fixture in document["fixtures"]:
        source_record = fixture["source"]
        if source_record["kind"] != "utf8":
            raise ValueError("this loader currently supports only UTF-8 text fixtures")
        source = source_record["text"].encode("utf-8")

        lex_result = fixture["expected"]["lex"]
        if lex_result["status"] != "success":
            raise ValueError("this loader currently supports only lexer success fixtures")

        tokens = tuple(
            Token(
                TokenKind(token["kind"]),
                token["lexeme"],
                SourceSpan(token["span"]["start_byte"], token["span"]["end_byte"]),
            )
            for token in lex_result["tokens"]
        )
        fixtures.append(
            LexerFixture(fixture["id"], source, LexSuccess(tokens))
        )

    return tuple(fixtures)
