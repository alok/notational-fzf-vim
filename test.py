#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shorten_path_for_notational_fzf as shorten_fzf
import sys

if __name__ == '__main__':
    for line in sys.stdin:
        shorten_fzf.process_line(line)

