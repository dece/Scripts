#!/usr/bin/env python3
"""Extract LSB plans for either RGB or the greyscale value. Requires Pillow."""

import sys

import PIL.Image

def main():
    img = PIL.Image.open(sys.argv[1])
    if img.mode == "L":
        print("Dumping grayscale LSB.")
        dump_monochannel(img)
    else:
        print("Dumping RGB LSB.")
        dump_rgb(img)

def dump_monochannel(img):
    width, height = img.size
    out = PIL.Image.new('1', (width, height))
    for x in range(width):
        for y in range(height):
            op = img.getpixel((x, y))
            p = 1 if op & 1 else 0
            out.putpixel((x, y), p)
    out.save("lsb.png")

def dump_rgb(img):
    width, height = img.size
    for i in range(3):
        out = PIL.Image.new('1', (width, height))
        for x in range(width):
            for y in range(height):
                op = img.getpixel((x, y))
                p = 1 if op[i] & 1 else 0
                out.putpixel((x, y), p)
        out.save(f"lsb{i}.png")

if __name__ == "__main__":
    main()
