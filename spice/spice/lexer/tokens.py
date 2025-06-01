"""Token definitions for Spice language."""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional


class TokenType(Enum):
    """Token types for Spice language."""

    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()

    # Keywords (Python)
    DEF = auto()
    CLASS = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    FOR = auto()
    WHILE = auto()
    RETURN = auto()
    IMPORT = auto()
    FROM = auto()
    AS = auto()
    WITH = auto()
    TRY = auto()
    EXCEPT = auto()
    FINALLY = auto()
    RAISE = auto()
    PASS = auto()
    BREAK = auto()
    CONTINUE = auto()
    TRUE = auto()
    FALSE = auto()
    NONE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    IN = auto()
    IS = auto()
    LAMBDA = auto()

    # New Keywords (Spice)
    INTERFACE = auto()
    ABSTRACT = auto()
    FINAL = auto()
    STATIC = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    DOUBLESTAR = auto()
    DOUBLESLASH = auto()
    EQUAL = auto()
    NOTEQUAL = auto()
    LESS = auto()
    GREATER = auto()
    LESSEQUAL = auto()
    GREATEREQUAL = auto()
    ASSIGN = auto()
    PLUSASSIGN = auto()
    MINUSASSIGN = auto()
    STARASSIGN = auto()
    SLASHASSIGN = auto()

    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    COLON = auto()
    SEMICOLON = auto()
    DOT = auto()
    ARROW = auto()

    # Special
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    EOF = auto()

    # Comments
    COMMENT = auto()


@dataclass
class Token:
    """Represents a token in the source code."""
    type: TokenType
    value: Any
    line: int
    column: int
    filename: Optional[str] = None

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, {self.line}, {self.column})"
