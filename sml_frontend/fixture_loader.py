"""Strict loading for the lexer conformance fixture slice."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any

from .lexer import LexSuccess
from .source import SourceSpan
from .token import Token, TokenKind


_FORMAT_VERSION = 1
_LANGUAGE_VERSION = "0.1"
_FIXTURE_ID = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z")


class FixtureFormatError(ValueError):
    """The fixture data violates the accepted version 1 structure."""


@dataclass(frozen=True, slots=True)
class LexerFixture:
    fixture_id: str
    source: bytes
    expected: LexSuccess


def load_lexer_success_fixtures(
    fixture_root: Path, relative_path: str
) -> tuple[LexerFixture, ...]:
    """Load one indexed lexer-success fixture file with strict field checks."""

    index = load_strict_json(fixture_root / "index.json")
    _require_exact_fields(
        index, {"format_version", "language_version", "fixture_files"}, "index"
    )
    _require_versions(index, "index")

    fixture_files = _require_unique_string_list(index["fixture_files"], "fixture_files")
    if relative_path not in fixture_files:
        raise FixtureFormatError(f"fixture file is not indexed: {relative_path}")

    fixture_path = _resolve_fixture_path(fixture_root, relative_path)
    document = load_strict_json(fixture_path)
    _require_exact_fields(
        document, {"format_version", "language_version", "fixtures"}, relative_path
    )
    _require_versions(document, relative_path)
    if not isinstance(document["fixtures"], list):
        raise FixtureFormatError(f"{relative_path}.fixtures must be an array")

    fixtures = tuple(
        _decode_lexer_success_fixture(value, f"{relative_path}.fixtures[{index}]")
        for index, value in enumerate(document["fixtures"])
    )
    fixture_ids = [fixture.fixture_id for fixture in fixtures]
    if len(fixture_ids) != len(set(fixture_ids)):
        raise FixtureFormatError(f"{relative_path} contains duplicate fixture IDs")
    return fixtures


def load_strict_json(path: Path) -> dict[str, Any]:
    """Load UTF-8 JSON while rejecting BOMs, duplicate keys, and nonobjects."""

    try:
        raw = path.read_bytes()
    except OSError as error:
        raise FixtureFormatError(f"cannot read fixture data: {path}") from error
    if raw.startswith(b"\xef\xbb\xbf"):
        raise FixtureFormatError(f"fixture JSON must not have a UTF-8 BOM: {path}")

    try:
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=_object_without_duplicate_keys
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise FixtureFormatError(f"invalid UTF-8 JSON: {path}") from error
    if not isinstance(value, dict):
        raise FixtureFormatError(f"fixture document must be an object: {path}")
    return value


def _decode_lexer_success_fixture(value: Any, context: str) -> LexerFixture:
    fixture = _require_object(value, context)
    _require_exact_fields(
        fixture,
        {"id", "description", "entrypoint", "source", "expected", "covers"},
        context,
    )

    fixture_id = fixture["id"]
    if not isinstance(fixture_id, str) or _FIXTURE_ID.fullmatch(fixture_id) is None:
        raise FixtureFormatError(f"{context}.id is invalid")
    if not isinstance(fixture["description"], str) or not fixture["description"]:
        raise FixtureFormatError(f"{context}.description must be nonempty")
    if fixture["entrypoint"] != "lexer":
        raise FixtureFormatError(f"{context}.entrypoint must be lexer")

    source = _decode_utf8_source(fixture["source"], f"{context}.source")
    expected = _decode_success_expectation(
        fixture["expected"], f"{context}.expected"
    )
    _validate_expected_tokens(source, expected.tokens, f"{context}.expected.lex.tokens")
    _validate_coverage(fixture["covers"], f"{context}.covers")
    return LexerFixture(fixture_id, source, expected)


def _decode_utf8_source(value: Any, context: str) -> bytes:
    source = _require_object(value, context)
    _require_exact_fields(source, {"kind", "text"}, context)
    if source["kind"] != "utf8" or not isinstance(source["text"], str):
        raise FixtureFormatError(f"{context} must be a utf8 text source")
    return source["text"].encode("utf-8")


def _decode_success_expectation(value: Any, context: str) -> LexSuccess:
    expected = _require_object(value, context)
    _require_exact_fields(expected, {"lex"}, context)
    lex_result = _require_object(expected["lex"], f"{context}.lex")
    _require_exact_fields(lex_result, {"status", "tokens"}, f"{context}.lex")
    if lex_result["status"] != "success" or not isinstance(lex_result["tokens"], list):
        raise FixtureFormatError(f"{context}.lex must be a success with tokens")
    tokens = tuple(
        _decode_token(token, f"{context}.lex.tokens[{index}]")
        for index, token in enumerate(lex_result["tokens"])
    )
    try:
        return LexSuccess(tokens)
    except ValueError as error:
        raise FixtureFormatError(f"{context}.lex has an invalid token collection") from error


def _decode_token(value: Any, context: str) -> Token:
    token = _require_object(value, context)
    _require_exact_fields(token, {"kind", "lexeme", "span"}, context)
    try:
        kind = TokenKind(token["kind"])
    except (TypeError, ValueError) as error:
        raise FixtureFormatError(f"{context}.kind is unknown") from error
    if not isinstance(token["lexeme"], str):
        raise FixtureFormatError(f"{context}.lexeme must be a string")

    span_data = _require_object(token["span"], f"{context}.span")
    _require_exact_fields(span_data, {"start_byte", "end_byte"}, f"{context}.span")
    start = span_data["start_byte"]
    end = span_data["end_byte"]
    if not _is_nonnegative_integer(start) or not _is_nonnegative_integer(end):
        raise FixtureFormatError(f"{context}.span boundaries must be nonnegative integers")
    try:
        return Token(kind, token["lexeme"], SourceSpan(start, end))
    except ValueError as error:
        raise FixtureFormatError(f"{context} is not a valid token") from error


def _validate_expected_tokens(
    source: bytes, tokens: tuple[Token, ...], context: str
) -> None:
    source_length = len(source)
    previous_end = 0

    for index, token in enumerate(tokens):
        token_context = f"{context}[{index}]"
        if token.span.end_byte > source_length:
            raise FixtureFormatError(
                f"{token_context}.span exceeds the source byte length"
            )
        if token.span.start_byte < previous_end:
            raise FixtureFormatError(
                f"{token_context}.span overlaps or precedes the previous token"
            )

        if token.kind is TokenKind.EOF:
            if token.span != SourceSpan(source_length, source_length):
                raise FixtureFormatError(
                    f"{token_context} must be physical EOF at the source byte length"
                )
        else:
            token_bytes = source[token.span.start_byte : token.span.end_byte]
            try:
                source_lexeme = token_bytes.decode("utf-8")
            except UnicodeDecodeError as error:
                raise FixtureFormatError(
                    f"{token_context}.span does not select complete UTF-8 text"
                ) from error
            if source_lexeme != token.lexeme:
                raise FixtureFormatError(
                    f"{token_context}.lexeme does not match its source span"
                )

        previous_end = token.span.end_byte


def _validate_coverage(value: Any, context: str) -> None:
    coverage = _require_object(value, context)
    fields = {"token_kinds", "ast_kinds", "diagnostic_codes", "rules"}
    _require_exact_fields(coverage, fields, context)
    for field in fields:
        _require_unique_string_list(coverage[field], f"{context}.{field}")


def _resolve_fixture_path(fixture_root: Path, relative_path: str) -> Path:
    if "\\" in relative_path or Path(relative_path).is_absolute():
        raise FixtureFormatError("fixture paths must be relative and use / separators")
    root = fixture_root.resolve()
    candidate = (root / relative_path).resolve()
    if candidate == root or root not in candidate.parents:
        raise FixtureFormatError("fixture path escapes the fixture directory")
    return candidate


def _object_without_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise FixtureFormatError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def _require_object(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise FixtureFormatError(f"{context} must be an object")
    return value


def _require_exact_fields(
    value: dict[str, Any], expected: set[str], context: str
) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        unknown = sorted(actual - expected)
        raise FixtureFormatError(
            f"{context} fields differ; missing={missing}, unknown={unknown}"
        )


def _require_versions(value: dict[str, Any], context: str) -> None:
    if value["format_version"] != _FORMAT_VERSION:
        raise FixtureFormatError(f"{context} has an unsupported format version")
    if value["language_version"] != _LANGUAGE_VERSION:
        raise FixtureFormatError(f"{context} has an unsupported language version")


def _require_unique_string_list(value: Any, context: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise FixtureFormatError(f"{context} must be an array of strings")
    if len(value) != len(set(value)):
        raise FixtureFormatError(f"{context} must not contain duplicates")
    return value


def _is_nonnegative_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0
