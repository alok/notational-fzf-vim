#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shorten file paths for notational-fzf-vim display.

Reads lines in format `filename:linenum:contents` from stdin,
outputs `filename:linenum:shortname:linenum:contents` with colored paths.
"""

from __future__ import annotations

import platform
import sys
from os import pardir
from os.path import abspath, expanduser, join, sep, split, splitdrive
from pathlib import PurePath

# ANSI color codes
GREEN = "\033[32m"
PURPLE = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"

# Path replacements (most restrictive first)
REPLACEMENTS = ("", pardir, "~")
OLD_PATHS = [abspath(expanduser(r)) for r in REPLACEMENTS]
IS_WINDOWS = platform.system().lower() == "windows"


def color(text: str, color_code: str) -> str:
    """Wrap text in ANSI color codes."""
    return f"{color_code}{text}{RESET}"


def prettyprint_path(path: str, old_path: str, replacement: str) -> str:
    """Replace path prefix and shorten remaining components to first char."""
    path = path.replace(old_path, replacement, 1)
    parts = PurePath(path).parts[1:]  # Skip the replacement prefix
    short_path = join(replacement, *(p[0] for p in parts))
    return short_path


def shorten(path: str) -> tuple[str, str]:
    """Returns shortened parent directory and filename."""
    path, filename = split(path)

    for replacement, old_path in zip(REPLACEMENTS, OLD_PATHS):
        if path.startswith(old_path):
            short_path = prettyprint_path(path, old_path, replacement)
            break
    else:
        # No replacement matched - shorten entire path
        parts = PurePath(path).parts
        short_path = join(*(p[0] for p in parts)) if parts else ""

    return short_path, filename


def process_line(line: str) -> str:
    """Process a single line from ripgrep output."""
    # Handle Windows drive letters (e.g., C:\path)
    if IS_WINDOWS:
        _, line = splitdrive(line)

    # Parse filename:linenum:contents
    try:
        filename, linenum, contents = line.split(sep=":", maxsplit=2)
    except ValueError:
        return line  # Return unchanged if format unexpected

    contents = contents.rstrip()

    # Normalize path (skip on Windows to avoid prepending cwd)
    if not IS_WINDOWS:
        filename = abspath(filename)

    shortened_parent, basename = shorten(filename)

    # Build colored short name
    if shortened_parent:
        colored_short_name = color(shortened_parent + sep, PURPLE) + color(basename, CYAN)
    else:
        colored_short_name = color(basename, CYAN)

    # Output format: long_path:linenum:short_path:linenum:contents
    return ":".join([
        color(filename, CYAN),
        color(linenum, GREEN),
        colored_short_name,
        color(linenum, GREEN),
        contents,
    ])


def main() -> None:
    """Read from stdin and process each line."""
    for raw_line in sys.stdin.buffer:
        try:
            line = raw_line.decode("utf-8")
            print(process_line(line))
        except UnicodeDecodeError:
            # Try latin-1 as fallback (can decode any byte sequence)
            try:
                line = raw_line.decode("latin-1")
                print(process_line(line))
            except Exception:
                pass  # Skip completely malformed lines
        except Exception:
            pass  # Skip lines that cause other errors


if __name__ == "__main__":
    main()
