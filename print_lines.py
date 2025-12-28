#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Colorize the current line in the preview window in bold red."""

import os.path as path
import shutil
import subprocess
import sys

# ANSI escape sequences
RED = "\033[1;31m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"


def count_lines(fname: str) -> int:
    """Count lines in a file, returning 0 on error."""
    try:
        with open(fname, encoding="utf-8", errors="replace") as f:
            return sum(1 for _ in f)
    except (OSError, IOError):
        return 0


def preview_with_bat(filepath: str, target_line: int, height: int) -> bool:
    """Preview file using bat. Returns True on success."""
    if not shutil.which("bat"):
        return False

    lines = count_lines(filepath)
    cmd = [
        "bat",
        "--style=numbers",
        "--color=always",
        f"--highlight-line={target_line}",
    ]

    # Center the view around the target line if possible
    if target_line > height // 2 and lines >= height:
        start = max(1, target_line - height // 2)
        cmd.append(f"--line-range={start}:{lines}")

    cmd.append(path.normpath(filepath))

    try:
        subprocess.run(cmd, check=False)
        return True
    except (OSError, subprocess.SubprocessError):
        return False


def preview_with_fallback(filepath: str, target_line: int, height: int) -> None:
    """Preview file with basic Python fallback (no bat)."""
    try:
        with open(path.normpath(filepath), encoding="utf-8", errors="replace") as f:
            lines = list(f)
    except (OSError, IOError):
        print(f"{RED}Error: Could not read file{RESET}")
        return

    # Calculate window around target line
    start = max(0, target_line - height // 2 - 1)
    end = min(len(lines), start + height)

    for i in range(start, end):
        linenum = i + 1
        content = lines[i].rstrip()
        if linenum == target_line:
            print(f"{BOLD}{RED}{content}{RESET}")
        else:
            print(content)


def main() -> None:
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <line> <file> <height>", file=sys.stderr)
        sys.exit(1)

    try:
        target_line = int(sys.argv[1])
        filepath = sys.argv[2]
        height = int(sys.argv[3])
    except ValueError as e:
        print(f"Error: Invalid argument: {e}", file=sys.stderr)
        sys.exit(1)

    if not preview_with_bat(filepath, target_line, height):
        preview_with_fallback(filepath, target_line, height)


if __name__ == "__main__":
    main()
