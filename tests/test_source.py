from dataclasses import FrozenInstanceError
import unittest

from sml_frontend.source import (
    PositionRange,
    SourceCursor,
    SourcePosition,
    SourceSpan,
    SourceUnitKind,
)


class SourceSpanTests(unittest.TestCase):
    def test_span_is_half_open_and_immutable(self) -> None:
        span = SourceSpan(2, 5)

        self.assertEqual(span.byte_length, 3)
        with self.assertRaises(FrozenInstanceError):
            span.end_byte = 6  # type: ignore[misc]

    def test_invalid_span_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            SourceSpan(-1, 0)
        with self.assertRaises(ValueError):
            SourceSpan(2, 1)

    def test_position_range_derives_its_byte_span(self) -> None:
        positions = PositionRange(
            SourcePosition(3, 2, 1),
            SourcePosition(5, 2, 3),
        )

        self.assertEqual(positions.span, SourceSpan(3, 5))


class SourceCursorTests(unittest.TestCase):
    def test_ascii_advances_one_byte_and_column(self) -> None:
        cursor = SourceCursor(b"a")

        unit = cursor.advance()

        self.assertEqual(unit.kind, SourceUnitKind.ASCII)
        self.assertEqual(unit.source_bytes, b"a")
        self.assertEqual(unit.positions.start, SourcePosition(0, 1, 1))
        self.assertEqual(unit.positions.end, SourcePosition(1, 1, 2))
        self.assertTrue(cursor.at_end)

    def test_lf_cr_and_crlf_each_advance_one_logical_line(self) -> None:
        cursor = SourceCursor(b"a\nb\rc\r\nd")
        units = []
        while not cursor.at_end:
            units.append(cursor.advance())

        newline_units = [unit for unit in units if unit.kind is SourceUnitKind.NEWLINE]
        self.assertEqual([unit.source_bytes for unit in newline_units], [b"\n", b"\r", b"\r\n"])
        self.assertEqual(cursor.position, SourcePosition(8, 4, 2))

    def test_tab_uses_four_column_stops(self) -> None:
        cursor = SourceCursor(b"\t123\t\t")

        first_tab = cursor.advance()
        cursor.advance()
        cursor.advance()
        cursor.advance()
        second_tab = cursor.advance()
        third_tab = cursor.advance()

        self.assertEqual(first_tab.positions.end.column, 5)
        self.assertEqual(second_tab.positions.start.column, 8)
        self.assertEqual(second_tab.positions.end.column, 9)
        self.assertEqual(third_tab.positions.start.column, 9)
        self.assertEqual(third_tab.positions.end.column, 13)

    def test_valid_multibyte_scalars_advance_one_column(self) -> None:
        source = "é😀".encode("utf-8")
        cursor = SourceCursor(source)

        first = cursor.advance()
        second = cursor.advance()

        self.assertEqual(first.kind, SourceUnitKind.UNICODE)
        self.assertEqual(first.span, SourceSpan(0, 2))
        self.assertEqual(first.positions.end.column, 2)
        self.assertEqual(second.kind, SourceUnitKind.UNICODE)
        self.assertEqual(second.span, SourceSpan(2, 6))
        self.assertEqual(second.positions.end.column, 3)

    def test_valid_utf8_boundary_scalars_are_consumed_whole(self) -> None:
        scalars = ["\u0800", "\ud7ff", "\ue000", "\U0010ffff"]

        for scalar in scalars:
            with self.subTest(code_point=hex(ord(scalar))):
                encoded = scalar.encode("utf-8")
                cursor = SourceCursor(encoded)

                unit = cursor.advance()

                self.assertEqual(unit.kind, SourceUnitKind.UNICODE)
                self.assertEqual(unit.source_bytes, encoded)
                self.assertEqual(unit.span, SourceSpan(0, len(encoded)))
                self.assertEqual(unit.positions.end.column, 2)
                self.assertTrue(cursor.at_end)

    def test_invalid_utf8_consumes_one_byte_and_column(self) -> None:
        cursor = SourceCursor(b"x\xffy")

        first = cursor.advance()
        invalid = cursor.advance()
        last = cursor.advance()

        self.assertEqual(first.kind, SourceUnitKind.ASCII)
        self.assertEqual(invalid.kind, SourceUnitKind.INVALID_UTF8)
        self.assertEqual(invalid.source_bytes, b"\xff")
        self.assertEqual(invalid.span, SourceSpan(1, 2))
        self.assertEqual(invalid.positions.end, SourcePosition(2, 1, 3))
        self.assertEqual(last.positions.start, SourcePosition(2, 1, 3))

    def test_overlong_surrogate_and_out_of_range_sequences_are_invalid(self) -> None:
        source = b"\xc0\x80\xed\xa0\x80\xf4\x90\x80\x80"
        cursor = SourceCursor(source)

        units = []
        while not cursor.at_end:
            units.append(cursor.advance())

        self.assertTrue(all(unit.kind is SourceUnitKind.INVALID_UTF8 for unit in units))
        self.assertEqual(len(units), len(source))

    def test_advance_at_eof_is_rejected(self) -> None:
        cursor = SourceCursor(b"")

        with self.assertRaises(EOFError):
            cursor.advance()


if __name__ == "__main__":
    unittest.main()
