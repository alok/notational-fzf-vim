#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Colorize the current line in the preview window in bold red."""

import os.path as path
import sys
import subprocess

line = int(sys.argv[1])
file = sys.argv[2]
height = int(sys.argv[3])


def opcount(fname):
    with open(fname) as f:
        for i, _ in enumerate(f):
            pass
    return i + 1


if __name__ == "__main__":
    try:
        # fail fast
        subprocess.check_call(["bat"])
        lines = opcount(file)
        cmd = [
            "bat",
            "--style=numbers",
            "--color=always",
            "--highlight-line={}".format(line),
        ]
        if (line > (height / 2)) and (lines >= height):
            cmd.append("--line-range={}:{}".format(int(line - (height / 2)), lines))
        cmd.append(path.normpath(file))
        subprocess.run(cmd)
    except Exception:
        is_sel = False
        # ANSI escape sequences for coloring matched line
        RED = "\033[1;31m"
        RESET = "\033[0;0m"
        BOLD = "\033[;1m"
        with open(path.normpath(file)) as f:
            for linenum, line_content in enumerate(f, start=1):
                if linenum == line:
                    print(BOLD + RED + line_content.rstrip() + RESET)
                    is_sel = True
                elif is_sel or (line - linenum <= (height / 2 - 1)):
                    print(line_content.rstrip())
