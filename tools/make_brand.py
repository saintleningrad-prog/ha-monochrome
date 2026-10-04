"""Generate brand icons for the Monochrome integration (no third-party libraries).

Draws a green CRT screen with scanlines and a pixel-art ">_" prompt on a transparent background.
Output: custom_components/monochrome/brand/icon.png (256x256) and icon@2x.png (512x512).
"""

import os
import struct
import zlib

GREEN = (0, 255, 65)
DARK = (0, 18, 6)
BG = (0, 0, 0, 0)

# 8x8 pixel glyphs: '>' and '_'
GLYPH_GT = ["X.......", ".XX.....", "...XX...", ".....XX.", "...XX...", ".XX.....", "X.......", "........"]
GLYPH_US = ["........"] * 7 + ["XXXXXXXX"]


def png(path, w, h, pixels):
    raw = b"".join(b"\x00" + bytes(c for px in row for c in px) for row in pixels)
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    data = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(data)


def draw(size):
    s = size / 256.0
    px = [[BG for _ in range(size)] for _ in range(size)]
    m, r, bw = int(16 * s), int(40 * s), int(10 * s)        # margin, corner radius, border width

    def inside_round(x, y, x0, y0, x1, y1, rad):
        cx = min(max(x, x0 + rad), x1 - rad)
        cy = min(max(y, y0 + rad), y1 - rad)
        return (x - cx) ** 2 + (y - cy) ** 2 <= rad * rad

    for y in range(size):
        for x in range(size):
            if inside_round(x, y, m, m, size - m, size - m, r):
                if inside_round(x, y, m + bw, m + bw, size - m - bw, size - m - bw, max(1, r - bw)):
                    shade = DARK if (y // max(1, int(3 * s))) % 2 else (0, 26, 9)   # scanlines
                    px[y][x] = shade + (255,)
                else:
                    px[y][x] = GREEN + (255,)

    cell = int(10 * s)                                       # size of one glyph pixel
    ox, oy = int(52 * s), int(88 * s)
    for gi, glyph in enumerate((GLYPH_GT, GLYPH_US)):
        for gy, line in enumerate(glyph):
            for gx, ch in enumerate(line):
                if ch != "X":
                    continue
                x0 = ox + gi * 9 * cell + gx * cell
                y0 = oy + gy * cell
                for y in range(y0, y0 + cell):
                    for x in range(x0, x0 + cell):
                        if 0 <= x < size and 0 <= y < size and (y // max(1, int(3 * s))) % 2 == 0:
                            px[y][x] = GREEN + (255,)
                        elif 0 <= x < size and 0 <= y < size:
                            px[y][x] = (0, 200, 52, 255)
    return px


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "custom_components", "monochrome", "brand")
    os.makedirs(out, exist_ok=True)
    for name, size in (("icon.png", 256), ("icon@2x.png", 512)):
        png(os.path.join(out, name), size, size, draw(size))
        print("written", name)
