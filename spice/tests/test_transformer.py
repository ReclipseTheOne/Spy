"""Tests for the Spy to Python transformer."""

from spice.lexer import Lexer
from spice.parser import Parser
from spice.transformer import Transformer


class TestTransformer:
    """Test transformer functionality."""

    def transform_source(self, source: str) -> str:
        """Helper to transform source code."""
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        parser = Parser()
        ast = parser.parse(tokens)
        transformer = Transformer()
        return transformer.transform(ast)

    def test_interface_to_protocol(self):
        """Test interface transformation to Protocol."""
        source = """interface Drawable {
    def draw(x: int, y: int) -> None;
}"""

        result = self.transform_source(source)

        assert "from typing import Protocol" in result
        assert "from abc import ABC, abstractmethod" in result
        assert "class Drawable(Protocol):" in result
        assert "@abstractmethod" in result
        assert "def draw(self, x: int, y: int) -> None:" in result
        assert "pass" in result

    def test_interface_with_inheritance(self):
        """Test interface with base transformation."""
        source = """interface Colorable(Drawable) {
    def set_color(color: str) -> None;
}"""

        result = self.transform_source(source)

        assert "class Colorable(Drawable, Protocol):" in result
        assert "def set_color(self, color: str) -> None:" in result

    def test_empty_interface(self):
        """Test empty interface transformation."""
        source = """interface Empty {
}"""

        result = self.transform_source(source)

        assert "class Empty(Protocol):" in result
        assert "pass" in result

    def test_multiple_methods(self):
        """Test interface with multiple methods."""
        source = """interface Shape {
    def area() -> float;
    def perimeter() -> float;
    def draw(x: int, y: int) -> None;
}"""

        result = self.transform_source(source)

        assert "def area(self) -> float:" in result
        assert "def perimeter(self) -> float:" in result
        assert "def draw(self, x: int, y: int) -> None:" in result
        assert result.count("@abstractmethod") == 3
        assert result.count("pass") == 3

    def test_no_imports_when_not_needed(self):
        """Test that imports are not added when not needed."""
        source = ""  # Empty file

        result = self.transform_source(source)

        assert "from typing import Protocol" not in result
        assert "from abc import ABC" not in result
        assert "from typing import final" not in result
