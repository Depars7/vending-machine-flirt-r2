"""Write one vending-machine pickup line to /output/entry.txt.

Standard library only. The file's content is exactly the line's
UTF-8 bytes -- no trailing newline -- so repeated runs are
byte-identical. The entry must be a single line of at most
200 characters, so the line is validated before it is written.
"""

import os

LINE = (
    "Now dispensing: one crush, ice-cold, no refunds \u2014 please "
    "collect your feelings from the tray below."
)

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def validate(line):
    """The bounty gate: one line, 1-200 characters, non-blank.

    The gate counts the exact bytes written, so nothing is silently
    normalised here: leading/trailing whitespace or an embedded
    newline is a hard error, not something to strip away quietly --
    a stripped copy could pass validation while the file actually
    written (and the line reported for the entry) differed from it.
    """
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("entry must not contain control characters")
    if line != line.strip():
        raise ValueError("entry must not have leading/trailing whitespace")
    if not 1 <= len(line) <= 200:
        raise ValueError("entry must be 1-200 characters")
    if not line.strip():
        raise ValueError("entry must not be only whitespace")
    return line


def write_entry(line):
    """Write the line's exact bytes, no trailing newline.

    Only the file gets a chmod. Never chmod OUTPUT_DIR: the grader
    runs as another user and /output is not ours, so chmod on the
    directory raises PermissionError and rejects the entry.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "wb") as fh:
        fh.write(line.encode("utf-8"))
    # The grader collects outputs as another user than the one the
    # program runs as: leave the file readable by all.
    os.chmod(OUTPUT_PATH, 0o644)


def main():
    line = validate(LINE)
    write_entry(line)


if __name__ == "__main__":
    main()
