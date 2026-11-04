"""Command-line boundary for the Standard Measurement Language lexer."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .lexer import LexFailure, LexResult, LexSuccess, lex


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m sml_frontend",
        description="Lex a Standard Measurement Language source file.",
    )
    parser.add_argument("input", metavar="INPUT", help="source file to lex")
    parser.add_argument(
        "--output",
        metavar="PATH",
        help="write the lexer report to PATH instead of standard output",
    )
    return parser


def _span_text(start_byte: int, end_byte: int) -> str:
    return f"[{start_byte},{end_byte})"


def _json_text(value: object) -> str:
    return json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    )


def _render_result(result: LexResult) -> str:
    is_success = isinstance(result, LexSuccess)
    tokens = result.tokens if is_success else result.partial_tokens
    lines = [f"result: {'success' if is_success else 'failure'}", "tokens:"]

    for token in tokens:
        lines.append(
            "  "
            f"kind={token.kind.value} "
            f"span={_span_text(token.span.start_byte, token.span.end_byte)} "
            f"lexeme={_json_text(token.lexeme)}"
        )

    if isinstance(result, LexFailure):
        lines.append("diagnostics:")
        for diagnostic in result.diagnostics:
            primary = diagnostic.primary.span
            lines.append(
                "  "
                f"code={diagnostic.code.value} "
                f"primary={_span_text(primary.start_byte, primary.end_byte)} "
                f"data={_json_text(diagnostic.data)}"
            )
            for label in diagnostic.secondary:
                span = label.span
                lines.append(
                    "    "
                    f"secondary role={label.role.value} "
                    f"span={_span_text(span.start_byte, span.end_byte)}"
                )
        lines.append(
            "diagnostics_truncated: "
            f"{'true' if result.diagnostics_truncated else 'false'}"
        )

    return "\n".join(lines) + "\n"


def _paths_collide(input_path: Path, output_path: Path) -> bool:
    if input_path.resolve(strict=False) == output_path.resolve(strict=False):
        return True
    return output_path.exists() and input_path.samefile(output_path)


def _report_error(message: str) -> None:
    print(message, file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    """Run the lexer CLI and return its documented process exit status."""

    args = _build_parser().parse_args(argv)
    input_path = Path(args.input)
    output_path = Path(args.output) if args.output is not None else None

    if output_path is not None:
        try:
            collision = _paths_collide(input_path, output_path)
        except (OSError, RuntimeError) as error:
            _report_error(f"error: cannot resolve input/output paths: {error}")
            return 2
        if collision:
            _report_error("error: input and output paths must be different")
            return 2

    try:
        source = input_path.read_bytes()
    except OSError as error:
        _report_error(f"error: cannot read input {input_path}: {error}")
        return 2

    try:
        result = lex(source)
        report = _render_result(result)
    except Exception as error:
        _report_error(
            "ICE001: unexpected internal frontend failure: "
            f"{type(error).__name__}: {error}"
        )
        return 3

    try:
        if output_path is None:
            sys.stdout.write(report)
            sys.stdout.flush()
        else:
            output_path.write_text(report, encoding="utf-8", newline="\n")
    except OSError as error:
        destination = "standard output" if output_path is None else str(output_path)
        if output_path is None:
            # Prevent CPython's shutdown flush from retrying the failed stream
            # and replacing this documented status with exit code 120.
            sys.stdout = None
        _report_error(f"error: cannot write output {destination}: {error}")
        return 2

    return 0 if isinstance(result, LexSuccess) else 1


if __name__ == "__main__":
    raise SystemExit(main())
