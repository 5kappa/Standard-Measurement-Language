"""Command-line tests for ``python -m sml_frontend``."""

from __future__ import annotations

import io
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from sml_frontend.__main__ import main


class CliTests(unittest.TestCase):
    def run_main(self, argv: list[str]) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = main(argv)
        return status, stdout.getvalue(), stderr.getvalue()

    def test_success_report_is_written_to_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory, "input.sml")
            input_path.write_bytes(b"let x = 1;")

            status, stdout, stderr = self.run_main([str(input_path)])

        self.assertEqual(status, 0)
        self.assertEqual(stderr, "")
        self.assertIn("result: success\n", stdout)
        self.assertIn('kind=LET span=[0,3) lexeme="let"\n', stdout)
        self.assertIn('kind=EOF span=[10,10) lexeme=""\n', stdout)

    def test_success_report_overwrites_named_output_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory, "input.sml")
            output_path = Path(temporary_directory, "report.txt")
            input_path.write_bytes(b"true")
            output_path.write_text("old report", encoding="utf-8")

            status, stdout, stderr = self.run_main(
                [str(input_path), "--output", str(output_path)]
            )
            report = output_path.read_text(encoding="utf-8")

        self.assertEqual(status, 0)
        self.assertEqual(stdout, "")
        self.assertEqual(stderr, "")
        self.assertIn('kind=TRUE span=[0,4) lexeme="true"\n', report)
        self.assertNotIn("old report", report)

    def test_lexical_failure_reports_partial_tokens_and_diagnostic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory, "invalid.sml")
            input_path.write_bytes(b"01 ok")

            status, stdout, stderr = self.run_main([str(input_path)])

        self.assertEqual(status, 1)
        self.assertEqual(stderr, "")
        self.assertIn("result: failure\n", stdout)
        self.assertIn('kind=IDENT span=[3,5) lexeme="ok"\n', stdout)
        self.assertIn(
            'code=LEX003 primary=[0,2) data={"candidate_lexeme":"01"}\n',
            stdout,
        )
        self.assertIn("diagnostics_truncated: false\n", stdout)

    def test_secondary_diagnostic_labels_are_rendered(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory, "invalid.sml")
            input_path.write_bytes(b"/*")

            status, stdout, _ = self.run_main([str(input_path)])

        self.assertEqual(status, 1)
        self.assertIn("code=LEX009 primary=[0,2) data={}\n", stdout)
        self.assertIn("secondary role=reached_eof span=[2,2)\n", stdout)

    def test_missing_input_file_is_an_io_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            missing_path = Path(temporary_directory, "missing.sml")

            status, stdout, stderr = self.run_main([str(missing_path)])

        self.assertEqual(status, 2)
        self.assertEqual(stdout, "")
        self.assertIn("error: cannot read input", stderr)

    def test_missing_required_input_argument_uses_argparse_exit_two(self) -> None:
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as raised:
                main([])

        self.assertEqual(raised.exception.code, 2)

    def test_output_write_failure_returns_exit_two(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory, "input.sml")
            output_directory = Path(temporary_directory, "output")
            input_path.write_bytes(b"false")
            output_directory.mkdir()

            status, stdout, stderr = self.run_main(
                [str(input_path), "--output", str(output_directory)]
            )

        self.assertEqual(status, 2)
        self.assertEqual(stdout, "")
        self.assertIn("error: cannot write output", stderr)

    def test_input_output_collision_is_rejected_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory, "input.sml")
            original_source = b"print 1;"
            input_path.write_bytes(original_source)

            status, stdout, stderr = self.run_main(
                [str(input_path), "--output", str(input_path)]
            )
            preserved_source = input_path.read_bytes()

        self.assertEqual(status, 2)
        self.assertEqual(stdout, "")
        self.assertIn("input and output paths must be different", stderr)
        self.assertEqual(preserved_source, original_source)

    def test_same_file_identity_collision_is_rejected_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory, "input.sml")
            output_path = Path(temporary_directory, "linked-output.txt")
            original_source = b"print 1;"
            input_path.write_bytes(original_source)
            output_path.write_text("existing output", encoding="utf-8")

            with patch("pathlib.Path.samefile", return_value=True):
                status, stdout, stderr = self.run_main(
                    [str(input_path), "--output", str(output_path)]
                )
            preserved_source = input_path.read_bytes()
            preserved_output = output_path.read_text(encoding="utf-8")

        self.assertEqual(status, 2)
        self.assertEqual(stdout, "")
        self.assertIn("input and output paths must be different", stderr)
        self.assertEqual(preserved_source, original_source)
        self.assertEqual(preserved_output, "existing output")

    def test_report_uses_stable_json_escaping_and_half_open_spans(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory, "input.sml")
            input_path.write_bytes(b'print "x";')

            status, stdout, stderr = self.run_main([str(input_path)])

        self.assertEqual(status, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(
            stdout,
            "result: success\n"
            "tokens:\n"
            '  kind=PRINT span=[0,5) lexeme="print"\n'
            '  kind=STRING span=[6,9) lexeme="\\\"x\\\""\n'
            '  kind=SEMICOLON span=[9,10) lexeme=";"\n'
            '  kind=EOF span=[10,10) lexeme=""\n',
        )

    def test_unexpected_frontend_failure_returns_exit_three(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory, "input.sml")
            input_path.write_bytes(b"true")

            with patch(
                "sml_frontend.__main__.lex",
                side_effect=RuntimeError("broken invariant"),
            ):
                status, stdout, stderr = self.run_main([str(input_path)])

        self.assertEqual(status, 3)
        self.assertEqual(stdout, "")
        self.assertIn("ICE001: unexpected internal frontend failure", stderr)
        self.assertIn("RuntimeError: broken invariant", stderr)

    def test_module_entry_point_runs_in_a_real_subprocess(self) -> None:
        repository_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory, "input.sml")
            input_path.write_bytes(b"const answer = 42;")

            completed = subprocess.run(
                [sys.executable, "-m", "sml_frontend", str(input_path)],
                cwd=repository_root,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stderr, "")
        self.assertIn("result: success\n", completed.stdout)
        self.assertIn('kind=NUMBER span=[15,17) lexeme="42"\n', completed.stdout)


if __name__ == "__main__":
    unittest.main()
