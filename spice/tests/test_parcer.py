"""Tests for the Spy parser."""

import pytest
from spice.lexer import Lexer
from spice.parser import Parser
from spice.parser.ast_nodes import InterfaceDeclaration


class TestParser:
    """Test parser functionality."""

    def parse_source(self, source: str):
        """Helper to parse source code."""
        lexer = Lexer()
        tokens = lexer.tokenize(source)
        parser = Parser()
        return parser.parse(tokens)

    def test_interface_declaration(self):
        """Test parsing interface declaration."""
        source = """interface Drawable {
    def draw(x: int, y: int) -> None;
    def get_bounds() -> tuple;
}"""

        ast = self.parse_source(source)

        assert len(ast.body) == 1
        interface = ast.body[0]

        assert isinstance(interface, InterfaceDeclaration)
        assert interface.name == "Drawable"
        assert len(interface.methods) == 2

        # Check first method
        draw_method = interface.methods[0]
        assert draw_method.name == "draw"
        assert len(draw_method.params) == 2
        assert draw_method.params[0].name == "x"
        assert draw_method.params[0].type_annotation == "int"
        assert draw_method.return_type == "None"

        # Check second method
        bounds_method = interface.methods[1]
        assert bounds_method.name == "get_bounds"
        assert len(bounds_method.params) == 0
        assert bounds_method.return_type == "tuple"

    def test_interface_with_inheritance(self):
        """Test interface with base interfaces."""
        source = """interface Colorable(Drawable) {
    def set_color(color: str) -> None;
}"""

        ast = self.parse_source(source)
        interface = ast.body[0]

        assert isinstance(interface, InterfaceDeclaration)
        assert interface.name == "Colorable"
        assert interface.base_interfaces == ["Drawable"]
        assert len(interface.methods) == 1

    def test_empty_interface(self):
        """Test empty interface parsing."""
        source = """interface Empty {
}"""

        ast = self.parse_source(source)
        interface = ast.body[0]

        assert isinstance(interface, InterfaceDeclaration)
        assert interface.name == "Empty"
        assert len(interface.methods) == 0

    def test_method_with_default_param(self):
        """Test method with default parameter."""
        source = """interface Example {
    def method(x: int, y: int = 0) -> int;
}"""

        ast = self.parse_source(source)
        interface = ast.body[0]
        method = interface.methods[0]

        assert len(method.params) == 2
        assert method.params[1].name == "y"
        assert method.params[1].default == "0"

    @pytest.mark.skip(reason="Python-style parsing not yet implemented")
    def test_python_style_interface(self):
        """Test Python-style interface declaration."""
        source = """interface Drawable:
    def draw(x: int, y: int) -> None
    def get_bounds() -> tuple"""

        ast = self.parse_source(source)
        interface = ast.body[0]

        assert isinstance(interface, InterfaceDeclaration)
        assert interface.name == "Drawable"
        assert len(interface.methods) == 2
