#!/usr/bin/env python3
# encoding: utf-8

import sys
import pathlib
import os

# Type alias.
Path = str


def expand_path(path: Path) -> Path:
    ''' Expand tilde and return absolute path. '''

    return os.path.abspath(os.path.expanduser(path))


def prettyprint_path(path: Path, old_path: Path, replacement: Path) -> Path:
    # Pretty print the path prefix
    path = path.replace(old_path, replacement, 1)
    # Truncate the rest of the path to a single character.
    short_path = os.path.join(
        replacement, * [x[0] for x in pathlib.PurePath(path).parts[1:]]
    )
    return short_path


def shorten(path: Path) -> Path:
    # We don't want to shorten the filename, just its parent directory, so we
    # `split()` and just shorten `path`.
    path, filename = os.path.split(path)

    # use empty replacement for current directory. it expands correctly
    replacements = ['', '..', '~']
    old_paths = [expand_path(replacement) for replacement in replacements]

    for replacement, old_path in zip(replacements, old_paths):
        if path.startswith(old_path):
            short_path = prettyprint_path(path, old_path, replacement)
            # to avoid multiple replacements
            break

    # If no replacement was found, shorten the entire path.
    else:
        short_path = os.path.join(
            * [x[0] for x in pathlib.PurePath(path).parts]
        )

    # This list will always have len 2, so we can unpack it.
    return os.path.join(short_path, filename)


if __name__ == '__main__':
    for line in sys.stdin:
        # Expected format is colon separated (name:linenum:contents)
        filename, linenum, contents = line.split(sep=':', maxsplit=2)

        # Normalize path for further processing.
        filename = expand_path(filename)

        # Drop trailing newline.
        contents = contents.rstrip()

        # We print the long and short forms, and one is picked in the Vim script
        # that uses this.
        print(
            # long form
            ':'.join([
                filename,
                linenum,
                # short form
            ] + [
                shorten(filename),
                linenum,
                # rest of line
            ] + [contents])
        )
