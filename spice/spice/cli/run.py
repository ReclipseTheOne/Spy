#!/usr/bin/env python3
"""Direct execution of .spy files."""

import click
import sys
import tempfile
import subprocess
from pathlib import Path
from typing import Optional

from lexer import Lexer
from parser.parser import Parser
from transformer.transformer import Transformer
from errors import SpiceError


@click.command()
@click.argument('source', type=click.Path(exists=True))
@click.option('-v', '--verbose', is_flag=True, help='Verbose output')
@click.option('--keep-temp', is_flag=True, help='Keep temporary Python file for debugging')
def run(source: str, verbose: bool, keep_temp: bool):
    """Run a .spy file directly without creating permanent Python files."""
    source_path = Path(source)

    if not source_path.suffix == '.spy':
        click.echo(f"Error: Expected .spy file, got {source_path.suffix}", err=True)
        sys.exit(1)

    try:        # Create temporary Python file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as temp_file:
            temp_path = Path(temp_file.name)

            if verbose:
                click.echo(f"🚀 Running {source_path}...")
                click.echo(f"📝 Temporary Python file: {temp_path}")

            # Compile spy to python
            compile_spy_file(source_path, temp_path, verbose)

            # Execute the Python file
            if verbose:
                click.echo(f"⚡ Executing compiled Python...")

            result = subprocess.run([sys.executable, str(temp_path)],
                                  capture_output=False, text=True)

            # Clean up temporary file unless keeping it
            if not keep_temp:
                try:
                    temp_path.unlink()
                except:
                    pass  # Ignore cleanup errors
            else:
                click.echo(f"📁 Temporary file kept at: {temp_path}")

            sys.exit(result.returncode)

    except SpiceError as e:
        click.echo(f"Compilation error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Runtime error: {e}", err=True)
        sys.exit(1)


def compile_spy_file(source_path: Path, output_path: Path, verbose: bool):
    """Compile a .spy file to Python."""
    # Read source
    with open(source_path, 'r', encoding='utf-8') as f:
        source_code = f.read()

    # Compilation pipeline
    lexer = Lexer()
    tokens = lexer.tokenize(source_code)

    parser = Parser()
    ast = parser.parse(tokens)

    transformer = Transformer()
    python_code = transformer.transform(ast)

    # Write compiled Python
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(python_code)


if __name__ == '__main__':
    run()
