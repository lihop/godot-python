import argparse
from pathlib import Path


HEADER = \
"""/**********************************************************/
/*       AUTOGENERATED FILE, DO NOT EDIT BY HAND !        */
/* Use tools/generate_bindings_header.py to regenerate it.*/
/**********************************************************/


#pragma once


#include "core/object.h"
"""
FOOTER = \
"""
"""


def _recursive_brute_force_includes(basedir, exclude=()):
    # Not proud about this...
    out = []
    for sub in basedir.iterdir():
        if sub.name in exclude:
            continue
        if sub.is_file() and sub.name.endswith('.h'):
            out.append(sub.name)
        elif sub.is_dir():
            for subsub in _recursive_brute_force_includes(sub):
                out.append('%s/%s' % (sub.name, subsub))
    return out


def _header_defines_godot_class(path):
    with open(path, 'r') as fd:
        for line in fd:
            if line.strip().startswith('GDCLASS('):
                return True
    return False


def main(root, outfd):
    headers = [h for h in _recursive_brute_force_includes(Path(root), exclude=['platform']) if _header_defines_godot_class(root + '/' + h)]
    outfd.write(HEADER + '\n'.join(['#include "%s"' % h for h in headers]) + FOOTER)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('godot_root', help='Path to Godot root dir.')
    parser.add_argument('--output', '-o', type=argparse.FileType('w'), default='bindings.gen.h',
                        help='Generated output (default: bindings.gen.h)')
    args = parser.parse_args()
    main(args.godot_root, args.output)
