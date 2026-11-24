"""The One-Line Exit entry for make.fun competition
u-kreutzx-the-one-line-exit-1dc652d1.

Writes one resignation letter, exactly one line long, to
$MAKEFUN_OUTPUT_DIR/entry.txt (fallback /output).

Pure Python stdlib, deterministic, no network, no reads outside the repo.
The program refuses to emit anything outside 1-140 characters, anything
that is not exactly one line, or anything that is only whitespace.
"""

import os
import sys

# The joke is a scale joke with the punchline in the last three words:
# eleven years guarding forty million dollars of stock, and the only
# thing that ever went missing was the guard's own lunch - stolen twice,
# and by the manager. The setup is a real letter (job, effective date,
# years of service, a number); the turn is that the thief is the boss.
LINE = (
    "I resign from nights, effective tonight: eleven years guarding "
    "$40M of stock, and the one thing stolen was my lunch, twice, "
    "by the manager."
)

MAX_CHARS = 140


def main():
    text = LINE.strip()

    if not 1 <= len(text) <= MAX_CHARS:
        print(
            "Refusing to emit: line is %d chars, must be 1-%d."
            % (len(text), MAX_CHARS),
            file=sys.stderr,
        )
        return 1

    if not text.strip():
        print("Refusing to emit: line is only whitespace.", file=sys.stderr)
        return 1

    if "\n" in text or "\r" in text:
        print("Refusing to emit: line must be exactly one line.",
              file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    # Verify what actually landed on disk: read it back as UTF-8 and
    # confirm it is still one line inside the 1-140 character gate, so
    # a bad write can never silently pass as a good entry.
    with open(out_path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text:
        print("Refusing to emit: written file does not match the line.",
              file=sys.stderr)
        return 1
    if not 1 <= len(written) <= MAX_CHARS or "\n" in written:
        print("Refusing to emit: written file fails the gate.",
              file=sys.stderr)
        return 1

    print("Wrote %s (%d chars, 1 line)." % (out_path, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
