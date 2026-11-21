#!/usr/bin/env python3
"""Cinnabar Reach Passport — Linnea Vance.

Round 3 entrypoint for make.fun bounty
the-passport-page-of-a-countr-2-20261121-0318.

Writes exactly one file, entry.png, into the output directory given by
MAKEFUN_OUTPUT_DIR (default /output). Standard library only, no network.
The image is a pre-rendered asset shipped next to this script; this program
only validates it against the competition's output rules and copies it.

Deliberately simple: no probe files, no temp files inside the output
directory, no fallback directory. If the output directory is not writable
the program fails loudly with a non-zero exit code instead of silently
writing somewhere the grader never looks.
"""

import os
import struct
import sys

MAX_BYTES = 1_048_576
MAX_DIMENSION = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
OUTPUT_FILENAME = "entry.png"


def fail(message):
    print("error: " + message, file=sys.stderr)
    return 1


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(script_dir, "entry.png")

    try:
        with open(source_path, "rb") as source_file:
            data = source_file.read()
    except OSError as exc:
        return fail("cannot read source image %s: %s" % (source_path, exc))

    if len(data) > MAX_BYTES:
        return fail("source image is %d bytes, over the %d byte limit"
                    % (len(data), MAX_BYTES))

    if data[:8] != PNG_MAGIC:
        return fail("source image is not a PNG (bad magic bytes)")

    if len(data) < 33 or data[12:16] != b"IHDR":
        return fail("source image has no valid PNG IHDR chunk")

    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        return fail("source image is %dx%d, over the %dx%d limit"
                    % (width, height, MAX_DIMENSION, MAX_DIMENSION))

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    output_path = os.path.join(output_dir, OUTPUT_FILENAME)

    try:
        with open(output_path, "wb") as output_file:
            output_file.write(data)
            output_file.flush()
            os.fsync(output_file.fileno())
    except OSError as exc:
        return fail("cannot write %s: %s" % (output_path, exc))

    # Confirm the file on disk is exactly what was validated above.
    try:
        written_size = os.path.getsize(output_path)
    except OSError as exc:
        return fail("cannot stat %s: %s" % (output_path, exc))
    if written_size != len(data):
        return fail("wrote %d bytes to %s, expected %d"
                    % (written_size, output_path, len(data)))

    try:
        os.chmod(output_path, 0o644)
    except OSError as exc:
        return fail("cannot chmod %s: %s" % (output_path, exc))

    print("wrote %s (%d bytes, %dx%d)" % (output_path, len(data), width, height))
    return 0


if __name__ == "__main__":
    sys.exit(main())
