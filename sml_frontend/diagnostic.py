"""Immutable structured lexical diagnostics."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .source import PositionRange, SourceSpan


class DiagnosticCode(Enum):
    LEX001 = "LEX001"
    LEX002 = "LEX002"
    LEX003 = "LEX003"
    LEX004 = "LEX004"
    LEX005 = "LEX005"
    LEX006 = "LEX006"
    LEX007 = "LEX007"
    LEX008 = "LEX008"
    LEX009 = "LEX009"
    LEX010 = "LEX010"


class DiagnosticPhase(Enum):
    LEXER = "LEXER"


class Severity(Enum):
    ERROR = "ERROR"


class LabelRole(Enum):
    PRIMARY = "PRIMARY"
    REACHED_EOF = "reached_eof"


DiagnosticValue = str | int | bool


@dataclass(frozen=True, slots=True)
class DiagnosticLabel:
    role: LabelRole
    span: SourceSpan
    positions: PositionRange | None = None

    def __post_init__(self) -> None:
        if self.positions is not None and self.positions.span != self.span:
            raise ValueError("label positions must match the label span")


@dataclass(frozen=True, slots=True)
class Diagnostic:
    code: DiagnosticCode
    primary: DiagnosticLabel
    secondary: tuple[DiagnosticLabel, ...] = ()
    notes: tuple[()] = ()
    data: dict[str, DiagnosticValue] = field(default_factory=dict)
    phase: DiagnosticPhase = DiagnosticPhase.LEXER
    severity: Severity = Severity.ERROR

    def __post_init__(self) -> None:
        if self.primary.role is not LabelRole.PRIMARY:
            raise ValueError("the primary label must use the PRIMARY role")
        if self.notes:
            raise ValueError("version 0.1 defines no structured diagnostic notes")
