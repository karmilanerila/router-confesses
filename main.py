"""The Router Confesses — make.fun bounty entry.

A home Wi-Fi router excuses itself for dying at the exact climax of a
movie. The angle: the router is not apologising for a failure at all.
It saw the killer's face a couple of seconds before the audience did
and chose to die rather than let the spoiler through — a smug little
secret, told in the router's own voice. No buffering, no bandwidth,
no firmware-update joke: the twist is that the outage was a favour.

The program writes exactly one line of text to /output/entry.txt.
It uses only the standard library, honours MAKEFUN_OUTPUT_DIR, writes
the file directly with open("wb") and chmod 0644, and never touches
anything outside the output directory.
"""

import os

# The confession, as the router would say it: a heroic sacrifice,
# delivered with the smugness of an appliance that knows something
# you do not. One line, well inside the 1-200 character gate.
CONFESSION = (
    "I glimpsed the killer's face two seconds early, "
    "so I died to spare you the spoiler. You're welcome."
)

MAX_CHARS = 200


def output_directory():
    """Return the directory the grader expects our text in."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if chosen:
        return chosen
    return "/output"


def entry_path(directory):
    """The single file the judge reads."""
    return os.path.join(directory, "entry.txt")


def check_line(line):
    """Keep the gate happy: 1-200 characters, one line, not blank."""
    stripped = line.strip()
    if not stripped:
        raise ValueError("confession must not be blank")
    if "\n" in line or "\r" in line:
        raise ValueError("confession must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError("confession is over 200 characters")
    return line


def write_entry(directory, line):
    """Write the line as UTF-8 bytes and make it readable."""
    os.makedirs(directory, exist_ok=True)
    path = entry_path(directory)
    data = line.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(data)
    os.chmod(path, 0o644)
    return path, len(line)


def verify_written(path, line):
    """Read the file back and confirm it holds exactly our line."""
    with open(path, "rb") as handle:
        stored = handle.read().decode("utf-8")
    if stored != line:
        raise ValueError("written entry does not match the confession")
    return len(stored)


def main():
    line = check_line(CONFESSION)
    directory = output_directory()
    path, chars = write_entry(directory, line)
    checked = verify_written(path, line)
    print("wrote {} ({} chars, verified {})".format(path, chars, checked))
    print(line)


if __name__ == "__main__":
    main()
