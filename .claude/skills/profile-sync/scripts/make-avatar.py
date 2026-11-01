#!/usr/bin/env python3
"""Build the upload sizes of the default profile picture from avatar/profile.jpeg.

    make-avatar.py

The source is 100x100. Sizes are square, centred and enlarged with Lanczos, so
they are softer than a real photo at that size. Needs Pillow.
"""

from biolib import ROOT, read_identity
from PIL import Image, ImageFilter

SIZES = (400, 800)


def main():
    source = ROOT / read_identity()["avatar"]
    img = Image.open(source).convert("RGB")
    side = min(img.size)
    left, top = (img.width - side) // 2, (img.height - side) // 2
    img = img.crop((left, top, left + side, top + side))
    for size in SIZES:
        out = source.parent / f"avatar-{size}.jpg"
        big = img.resize((size, size), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=size / 100, percent=60))
        big.save(out, quality=90, optimize=True)
        print(f"{out.relative_to(ROOT)}: {size}x{size}, {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
