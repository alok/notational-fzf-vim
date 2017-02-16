#!/usr/bin/env python
# encoding: utf-8

import sys


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
    filename = filename.split("/")[1:]
    print(
        pathify(filename) + ':' + linenum + ':' + shorten(filename) + ':' +
        linenum + ':' + contents
    )
