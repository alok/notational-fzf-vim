#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Colorize the current line in the preview window in bold red."""

import os.path as path
import sys

line = int(sys.argv[1])
file = sys.argv[2]
height = int(sys.argv[3])

# ANSI escape sequences for coloring matched line
RED = "\033[1;31m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"

if __name__ == "__main__":
    is_sel = False
    with open(path.normpath(file)) as f:
        for linenum, line_content in enumerate(f, start=1):
            if linenum == line:
                print(BOLD + RED + line_content.rstrip() + RESET)
                is_sel = True
            elif is_sel or (line - linenum <= (height / 2 - 1)):
                    print(line_content.rstrip())
