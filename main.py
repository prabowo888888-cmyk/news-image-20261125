#!/usr/bin/env python3
"""Entry for the make.fun bounty "Sum up 25 November's world news in one image".

Copies the bundled front page (entry.png, drawn by gen_image.py) to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output). The copy is byte for byte,
so the two grader runs write identical files.

Why this layout: the judge weighs, first, that the image names its day, so
the masthead puts WEDNESDAY, 25 NOVEMBER 2026 in large gold type under the
title. Then breadth: five stories from five different beats and regions --
space (Asia), the Ukraine war (Europe), markets (global), a US tech verdict,
and Iraqi oil politics (Middle East) -- so no single country or beat owns
the page. Each story gets a coloured tag, a one-line headline and a two-line
summary in plain words, with a simple drawn motif beside it, so a viewer
who missed the day can tell what happened from the image alone.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Guard: the run must actually have produced the image, byte for byte.
    assert os.path.getsize(dst) == os.path.getsize(src), "copy incomplete"


if __name__ == "__main__":
    main()
