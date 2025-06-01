"""Tests for the Spy lexer."""

import pytest
from spice.lexer import Lexer, TokenType


class TestLexer:
    """Test lexer functionality."""

    def test_keywords(self):
        """Test tokenization of Spy keywords."""
        lexer = Lexer()
        source = "interface abstract final static class def"
        tokens = lexer.tokenize(source)

        expected_types = [
            TokenType.INTERFACE,
            TokenType.ABSTRACT,
            TokenType.FINAL,
            TokenType.STATIC,
            TokenType.CLASS,
            TokenType.DEF,
            TokenType.NEWLINE,
            TokenType.EOF
        ]

        assert len(tokens) == len(expected_types)
        for token, expected_type in zip(tokens, expected_types):
            assert token.type == expected_type

    def test_interface_declaration(self):
        """Test interface declaration tokenization."""
        lexer = Lexer()
        source = """interface Drawable {
    def draw() -> None;
}"""
        tokens = lexer.tokenize(source)

        # Check key tokens
        assert tokens[0].type == TokenType.INTERFACE
        assert tokens[1].type == TokenType.IDENTIFIER
        assert tokens[1].value == "Drawable"
        assert tokens[2].type == TokenType.LBRACE

        # Find semicolon
        semicolon_found = any(t.type == TokenType.SEMICOLON for t in tokens)
        assert semicolon_found

    def test_numbers_and_strings(self):
        """Test number and string tokenization."""
        lexer = Lexer()
        source = '42 3.14 "hello" \'world\''
        tokens = lexer.tokenize(source)

        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == "42"
        assert tokens[1].type == TokenType.NUMBER
        assert tokens[1].value == "3.14"
        assert tokens[2].type == TokenType.STRING
        assert tokens[3].type == TokenType.STRING

    def test_operators(self):
        """Test operator tokenization."""
        lexer = Lexer()
        source = "+ - * / == != <= >= = += -="
        tokens = lexer.tokenize(source)

        expected_types = [
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.STAR,
            TokenType.SLASH,
            TokenType.EQUAL,
            TokenType.NOTEQUAL,
            TokenType.LESSEQUAL,
            TokenType.GREATEREQUAL,
            TokenType.ASSIGN,
            TokenType.PLUSASSIGN,
            TokenType.MINUSASSIGN,
        ]

        for i, expected_type in enumerate(expected_types):
            assert tokens[i].type == expected_type

    def test_comments(self):
        """Test comment handling."""
        lexer = Lexer()
        source = """# This is a comment
x = 5  # inline comment"""
        tokens = lexer.tokenize(source)

        # Comments should be tokenized but can be filtered later
        # Check that identifier 'x' is present
        identifier_tokens = [t for t in tokens if t.type == TokenType.IDENTIFIER]
        assert len(identifier_tokens) == 1
        assert identifier_tokens[0].value == "x"

    def test_multiline_code(self):
        """Test multiline code tokenization."""
        lexer = Lexer()
        source = """class Example:
    def method(self):
        return 42"""

        tokens = lexer.tokenize(source)

        # Verify structure
        assert tokens[0].type == TokenType.CLASS
        assert tokens[1].type == TokenType.IDENTIFIER
        assert tokens[1].value == "Example"
        assert tokens[2].type == TokenType.COLON

        # Find 'def' token
        def_tokens = [t for t in tokens if t.type == TokenType.DEF]
        assert len(def_tokens) == 1

    def test_error_on_invalid_character(self):
        """Test error handling for invalid characters."""
        lexer = Lexer()
        source = "valid @ invalid"

        with pytest.raises(SyntaxError):
            lexer.tokenize(source)
