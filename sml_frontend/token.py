"""Immutable lexer tokens."""

from dataclasses import dataclass
from enum import Enum

from .source import SourceSpan


class TokenKind(Enum):
    """Token kinds required by the first lexer pilot."""

    NUMBER = "NUMBER"
    IDENT = "IDENT"
    EOF = "EOF"


@dataclass(frozen=True, slots=True)
class Token:
    kind: TokenKind
    lexeme: str
    span: SourceSpan

    def __post_init__(self) -> None:
        if self.kind is TokenKind.EOF:
            if self.lexeme != "" or self.span.byte_length != 0:
                raise ValueError("EOF must have an empty lexeme and zero-width span")
            return

        if not self.lexeme or self.span.byte_length == 0:
            raise ValueError("non-EOF tokens require a lexeme and nonempty span")
        if len(self.lexeme.encode("utf-8")) != self.span.byte_length:
            raise ValueError("token lexeme bytes must exactly fill the token span")
