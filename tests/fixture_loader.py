"""Read trusted lexer fixtures into the records used by conformance tests."""

from __future__ import annotations

from collections.abc import Collection
from dataclasses import dataclass
import json
from pathlib import Path

from sml_frontend.lexer import LexSuccess
from sml_frontend.source import (
    PositionRange,
    SourceCursor,
    SourcePosition,
    SourceSpan,
)
from sml_frontend.token import Token, TokenKind


@dataclass(frozen=True, slots=True)
class LexerFixture:
    fixture_id: str
    source: bytes
    expected: LexSuccess
    expected_positions: tuple[PositionRange | None, ...]


def load_lexer_success_fixtures(
    path: Path, fixture_ids: Collection[str] | None = None
) -> tuple[LexerFixture, ...]:
    """Decode the trusted UTF-8 lexer-success fixtures in ``path``."""

    with path.open(encoding="utf-8") as fixture_file:
        document = json.load(fixture_file)

    if document["format_version"] != 1 or document["language_version"] != "0.1":
        raise ValueError("unsupported fixture format or language version")

    selected_ids = None if fixture_ids is None else set(fixture_ids)
    fixtures = []
    for fixture in document["fixtures"]:
        if selected_ids is not None and fixture["id"] not in selected_ids:
            continue

        source_record = fixture["source"]
        if source_record["kind"] != "utf8":
            raise ValueError("this loader currently supports only UTF-8 text fixtures")
        source = source_record["text"].encode("utf-8")

        lex_result = fixture["expected"]["lex"]
        if lex_result["status"] != "success":
            raise ValueError("this loader currently supports only lexer success fixtures")

        tokens = []
        expected_positions = []
        for token in lex_result["tokens"]:
            tokens.append(
                Token(
                    TokenKind(token["kind"]),
                    token["lexeme"],
                    SourceSpan(
                        token["span"]["start_byte"],
                        token["span"]["end_byte"],
                    ),
                )
            )
            positions = token.get("positions")
            expected_positions.append(
                None if positions is None else _decode_position_range(positions)
            )
        fixtures.append(
            LexerFixture(
                fixture["id"],
                source,
                LexSuccess(tuple(tokens)),
                tuple(expected_positions),
            )
        )

    if selected_ids is not None:
        loaded_ids = {fixture.fixture_id for fixture in fixtures}
        missing_ids = selected_ids - loaded_ids
        if missing_ids:
            raise ValueError(f"fixture IDs not found in {path}: {sorted(missing_ids)}")

    return tuple(fixtures)


def locate_token_positions(
    source: bytes, tokens: tuple[Token, ...]
) -> tuple[PositionRange, ...]:
    """Locate actual token-span boundaries without expanding the public token API."""

    cursor = SourceCursor(source)
    positions_by_offset = {0: cursor.position}
    while not cursor.at_end:
        cursor.advance()
        positions_by_offset[cursor.offset] = cursor.position

    return tuple(
        PositionRange(
            positions_by_offset[token.span.start_byte],
            positions_by_offset[token.span.end_byte],
        )
        for token in tokens
    )


def _decode_position_range(record: dict[str, object]) -> PositionRange:
    start = record["start"]
    end = record["end"]
    if not isinstance(start, dict) or not isinstance(end, dict):
        raise ValueError("fixture position boundaries must be records")
    return PositionRange(_decode_position(start), _decode_position(end))


def _decode_position(record: dict[str, object]) -> SourcePosition:
    return SourcePosition(
        int(record["byte_offset"]),
        int(record["line"]),
        int(record["column"]),
    )
