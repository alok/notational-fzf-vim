#!/usr/bin/env python3
"""
Unique file search for notational-fzf-vim.
Searches filenames and content, returns unique files sorted by mtime.

Usage: unique_files_search.py <query> <path1> [path2] ...

If query is empty, returns all files sorted by mtime (most recent first).
Otherwise, searches both filenames and file contents, deduplicates, and
returns results sorted by mtime.
"""

import os
import sys
import subprocess
from pathlib import Path


def get_files_sorted_by_mtime(paths):
    """Get all files in paths, sorted by modification time (newest first)."""
    files = []
    for path in paths:
        p = Path(path).expanduser()
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            for f in p.rglob('*'):
                if f.is_file() and not any(part.startswith('.') for part in f.parts):
                    files.append(f)

    # Sort by mtime, newest first
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return files


def search_filenames(query, files):
    """Return files whose names contain the query (case-insensitive)."""
    query_lower = query.lower()
    return [f for f in files if query_lower in f.name.lower()]


def search_content(query, paths):
    """Use ripgrep to find files containing the query."""
    try:
        result = subprocess.run(
            ['rg', '-l', '-i', '--no-messages', query] + paths,
            capture_output=True,
            text=True
        )
        return [Path(line) for line in result.stdout.strip().split('\n') if line]
    except Exception:
        return []


def main():
    if len(sys.argv) < 3:
        print("Usage: unique_files_search.py <query> <path1> [path2] ...", file=sys.stderr)
        sys.exit(1)

    query = sys.argv[1]
    paths = sys.argv[2:]

    # Get all files sorted by mtime
    all_files = get_files_sorted_by_mtime(paths)

    if not query:
        # No query - return all files sorted by mtime
        for f in all_files:
            print(str(f))
    else:
        # Search both filenames and content
        filename_matches = set(str(f) for f in search_filenames(query, all_files))
        content_matches = set(str(f) for f in search_content(query, paths))

        # Union of matches
        all_matches = filename_matches | content_matches

        # Filter and maintain mtime order
        seen = set()
        for f in all_files:
            f_str = str(f)
            if f_str in all_matches and f_str not in seen:
                print(f_str)
                seen.add(f_str)

        # Also suggest creating a new file with the query as name
        # (This will be filtered by fzf if it doesn't match)
        main_dir = Path(paths[0]).expanduser()
        if main_dir.is_dir():
            new_file = main_dir / f"{query}.md"
            if str(new_file) not in seen:
                print(str(new_file))


if __name__ == '__main__':
    main()
