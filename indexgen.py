#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import functools
AUTOGEN_MARKER = "AUTOGEN_MARKER"
hiddens = ['000']
openu = functools.partial(open, encoding='utf-8')


def incl_md(fpath, fout):
    with openu(fpath, 'r') as fin:
        for line in fin:
            if line.startswith(AUTOGEN_MARKER):
                break
            fout.write(line)


def write_item(id, base_name, dir_name, file_name, fout):
    with openu(os.path.join(os.path.join(base_name, dir_name), file_name), 'r') as fin:
        for line in fin:
            match = re.match(write_item.pattern_title, line)
            if match is not None:
                fout.write("%d. [%s](./%s/%s)\n\n" %
                           (int(id), match.group(1), dir_name, file_name))
                return


write_item.pattern_title = re.compile(r'#\s+(.+)')


def __main__():
    base_dir = "."
    fout = openu(os.path.join(base_dir, "index.md"), 'w')
    incl_md(os.path.join(base_dir, "index-header.md"), fout)
    pattern = re.compile(r'([0-9]+)-.+\.md')
    dir_articles = "articles"
    for fname in sorted(os.listdir(os.path.join(base_dir, dir_articles))):
        match = re.match(pattern, fname)
        if match is None or match.group(1) in hiddens:
            continue
        write_item(match.group(1), base_dir, dir_articles, fname, fout)
    incl_md(".\\index-footer.md", fout)
    fout.close()


if __name__ == '__main__':
    __main__()
