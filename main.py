#!/usr/bin/env python3
"""Write the warning label to $MAKEFUN_OUTPUT_DIR/entry.txt.

Stdlib only, no network, no arguments, exit 0, deterministic.
"""

import os
import sys

LABEL = (
    "WARNING: This human has read none of the instructions, "
    "understood all of them, and will now explain them to you."
)


def validate(label: str) -> str:
    """Check the label against the gate; return an error message or ""."""
    if "\n" in label or "\r" in label:
        return "label must be a single line"
    if not 1 <= len(label) <= 160:
        return f"label is {len(label)} characters, must be 1-160"
    if not label.strip():
        return "label must not be only whitespace"
    return ""


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    # Gate: exactly one line, 1-160 characters, not only whitespace.
    error = validate(LABEL)
    if error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    data = LABEL.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)

    # Read back and verify byte-identical.
    with open(path, "rb") as f:
        if f.read() != data:
            print("error: read-back mismatch", file=sys.stderr)
            return 1

    print(f"Wrote {path} ({len(LABEL)} characters): {LABEL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
