"""Immutable lexer tokens."""

from dataclasses import dataclass
from enum import Enum

from .source import SourceSpan


class TokenKind(Enum):
    """Complete Standard Measurement Language version 0.1 token inventory."""

    NUMBER = "NUMBER"
    STRING = "STRING"
    IDENT = "IDENT"

    TRUE = "TRUE"
    FALSE = "FALSE"

    LET = "LET"
    CONST = "CONST"
    FN = "FN"
    RETURN = "RETURN"
    IF = "IF"
    ELSE = "ELSE"
    FOR = "FOR"
    WHILE = "WHILE"
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"
    PRINT = "PRINT"
    INPUT = "INPUT"
    ASSERT = "ASSERT"
    AS = "AS"
    INT = "INT"
    FLOAT = "FLOAT"
    BOOL = "BOOL"
    TEXT = "TEXT"
    LENGTH = "LENGTH"
    MASS = "MASS"
    TIME = "TIME"
    FORCE = "FORCE"
    TO = "TO"
    THEN = "THEN"
    DO = "DO"

    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"
    PERCENT = "PERCENT"
    CARET = "CARET"
    BANG = "BANG"

    PLUS_PLUS = "PLUS_PLUS"
    MINUS_MINUS = "MINUS_MINUS"

    ASSIGN = "ASSIGN"
    PLUS_ASSIGN = "PLUS_ASSIGN"
    MINUS_ASSIGN = "MINUS_ASSIGN"
    STAR_ASSIGN = "STAR_ASSIGN"
    SLASH_ASSIGN = "SLASH_ASSIGN"

    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    BANG_EQUAL = "BANG_EQUAL"

    AND_AND = "AND_AND"
    OR_OR = "OR_OR"

    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    SEMICOLON = "SEMICOLON"
    COLON = "COLON"
    COMMA = "COMMA"

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
