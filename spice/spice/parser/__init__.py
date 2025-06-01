"""Parser module for Spy language."""

from .parser import Parser

# The only place where I'll actaully use *
from .ast_nodes import *

__all__ = ['Parser']
