"""News-image entry: copy the finished front page to /output/entry.png.

The image is entry.png beside this file, drawn by draw_image.py for
Sunday 22 November 2026. Standard library only, no network, and the
same bytes are written on every run.
"""
import os
import shutil

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "entry.png")
dst = os.path.join(out_dir, "entry.png")
if not os.path.isfile(src):
    raise SystemExit("entry.png is missing from the repository")
shutil.copyfile(src, dst)
