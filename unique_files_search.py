#!/usr/bin/env python3
"""
Unique file search for notational-fzf-vim.
Searches filenames and content, returns unique files sorted by mtime.

Usage: unique_files_search.py <query> <path1> [path2] ...

If query is empty, returns all files sorted by mtime (most recent first).
Otherwise, searches both filenames and file contents, deduplicates, and
returns results sorted by mtime.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Iterable


def get_mtime_safe(filepath: Path) -> float:
    """Get mtime, returning 0 for inaccessible files."""
    try:
        return filepath.stat().st_mtime
    except (OSError, PermissionError):
        return 0.0


def list_files_with_rg(directory: Path) -> list[Path]:
    """List files using ripgrep (respects .gitignore)."""
    try:
        result = subprocess.run(
            ["rg", "--files", str(directory)],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return [Path(line) for line in result.stdout.splitlines() if line]
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return []


def list_files_fallback(directory: Path) -> list[Path]:
    """List files using pathlib (fallback when rg unavailable)."""
    files = []
    try:
        for f in directory.rglob("*"):
            try:
                if f.is_file():
                    files.append(f)
            except (OSError, PermissionError):
                continue
    except (OSError, PermissionError):
        pass
    return files


def get_files_sorted_by_mtime(search_paths: list[str]) -> list[Path]:
    """Get all files in paths, sorted by modification time (newest first)."""
    files: list[Path] = []

    for search_path in search_paths:
        try:
            p = Path(search_path).expanduser().resolve()
        except (OSError, PermissionError):
            continue

        if p.is_file():
            files.append(p)
        elif p.is_dir():
            # Try rg first, fall back to pathlib
            dir_files = list_files_with_rg(p)
            if not dir_files:
                dir_files = list_files_fallback(p)
            files.extend(dir_files)

    # Sort by mtime, newest first
    files.sort(key=get_mtime_safe, reverse=True)
    return files


def search_paths_and_names(query: str, files: Iterable[Path]) -> list[Path]:
    """Return files whose path or name contains the query (case-insensitive)."""
    query_lower = query.lower()
    matches = []
    for f in files:
        # Search both filename and full path
        if query_lower in f.name.lower() or query_lower in str(f).lower():
            matches.append(f)
    return matches


def search_content(query: str, search_paths: list[str]) -> list[Path]:
    """Use ripgrep to find files containing the query."""
    try:
        result = subprocess.run(
            ["rg", "-l", "-i", "--no-messages", "--", query] + search_paths,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return [Path(line).resolve() for line in result.stdout.splitlines() if line]
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return []


def resolve_safe(filepath: Path) -> str | None:
    """Resolve path safely, returning None on error."""
    try:
        return str(filepath.resolve())
    except (OSError, PermissionError):
        return None


def main() -> None:
    if len(sys.argv) < 3:
        print(
            "Usage: unique_files_search.py <query> <path1> [path2] ...",
            file=sys.stderr,
        )
        sys.exit(1)

    query = sys.argv[1]
    search_paths = sys.argv[2:]

    # Get all files sorted by mtime
    all_files = get_files_sorted_by_mtime(search_paths)

    if not query:
        # No query - return all files sorted by mtime
        for f in all_files:
            print(f)
    else:
        # Search both paths/names and content
        path_matches = {resolve_safe(f) for f in search_paths_and_names(query, all_files)}
        content_matches = {resolve_safe(f) for f in search_content(query, search_paths)}

        # Union of matches (excluding None from failed resolves)
        all_matches = (path_matches | content_matches) - {None}

        # Filter and maintain mtime order
        seen: set[str] = set()
        for f in all_files:
            resolved = resolve_safe(f)
            if resolved and resolved in all_matches and resolved not in seen:
                print(resolved)
                seen.add(resolved)


if __name__ == "__main__":
    main()
