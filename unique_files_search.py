#!/usr/bin/env python3
"""
Unique file search for notational-fzf-vim.
Searches filenames and content, returns unique files sorted by mtime.

Usage: unique_files_search.py <query> <path1> [path2] ...

If query is empty, returns all files sorted by mtime (most recent first).
Otherwise, searches both filenames and file contents, deduplicates, and
returns results sorted by mtime.
"""

import sys
import subprocess
from pathlib import Path


def get_mtime_safe(f):
    """Get mtime, returning 0 for inaccessible files."""
    try:
        return f.stat().st_mtime
    except (OSError, PermissionError):
        return 0


def get_files_sorted_by_mtime(paths):
    """Get all files in paths, sorted by modification time (newest first)."""
    files = []
    for path in paths:
        try:
            p = Path(path).expanduser().resolve()
        except (OSError, PermissionError):
            continue

        if p.is_file():
            files.append(p)
        elif p.is_dir():
            try:
                # Use rg --files to respect .gitignore
                result = subprocess.run(
                    ['rg', '--files', str(p)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                for line in result.stdout.strip().split('\n'):
                    if line:
                        files.append(Path(line))
            except (subprocess.TimeoutExpired, FileNotFoundError):
                # Fallback to rglob if rg fails
                for f in p.rglob('*'):
                    try:
                        if f.is_file():
                            files.append(f)
                    except (OSError, PermissionError):
                        continue

    # Sort by mtime, newest first
    files.sort(key=get_mtime_safe, reverse=True)
    return files


def search_filenames(query, files):
    """Return files whose names contain the query (case-insensitive)."""
    query_lower = query.lower()
    return [f for f in files if query_lower in f.name.lower()]


def search_content(query, paths):
    """Use ripgrep to find files containing the query."""
    try:
        result = subprocess.run(
            ['rg', '-l', '-i', '--no-messages', '--', query] + paths,
            capture_output=True,
            text=True,
            timeout=30
        )
        return [Path(line).resolve() for line in result.stdout.strip().split('\n') if line]
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
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
        filename_matches = set(str(f.resolve()) for f in search_filenames(query, all_files))
        content_matches = set(str(f) for f in search_content(query, paths))

        # Union of matches
        all_matches = filename_matches | content_matches

        # Filter and maintain mtime order, normalize paths for comparison
        seen = set()
        for f in all_files:
            try:
                f_resolved = str(f.resolve())
            except (OSError, PermissionError):
                continue
            if f_resolved in all_matches and f_resolved not in seen:
                print(f_resolved)
                seen.add(f_resolved)


if __name__ == '__main__':
    main()
