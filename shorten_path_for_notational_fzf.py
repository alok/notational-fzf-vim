#!/usr/bin/env python
# encoding: utf-8

import sys
from os.path import dirname, abspath


def shorten(path):
    # input: list
    # out: str (shortened filepath)

    return "/" + "/".join([x[0] for x in path[:-1]]) + "/" + path[-1]


def pathify(path):
    return '/' + '/'.join(path)


for line in sys.stdin:
    # name: linenum: contents
    filename, linenum, contents = line.split(':', 2)
    # drop trailing newline
    contents = contents[:-1]

    # for files that start with a dot or double dot for current or parent dir
    # 3 cases:

    # notes.md
    # ./notes.md
    # ../notes.md

    # handle ../ first, then fall through to ./, then bare name

    if filename[0] != '/':
        if filename[0:2] == '..':
            # [2:] since [1] is a dot that should be stripped
            filename = dirname(abspath('.')) + filename[2:]
        elif filename[0] == '.':
            filename = abspath('.') + filename[1:]
        else:
            filename = abspath('.') + '/' + filename

    filename = filename.split("/")[1:]
    print(
        pathify(filename) + ':' + linenum + ':' + shorten(filename) + ':' +
        linenum + ':' + contents
    )
