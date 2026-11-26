#!/usr/bin/env python3
"""Append a short listening note to a private Markdown file."""

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("note", help="one line, optionally starting with the playlist name")
    parser.add_argument("--file", type=Path, default=Path(".playlist-organizer/feedback.md"),
                        help="private notes file (default .playlist-organizer/feedback.md)")
    args = parser.parse_args()
    note = args.note.strip()
    if not note or len(note.splitlines()) != 1:
        parser.error("enter one nonempty line")
    path = args.file.expanduser()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a+b") as notes:
            prefix = b""
            if notes.tell():
                notes.seek(-1, 2)
                if notes.read(1) != b"\n":
                    prefix = b"\n"
            notes.write(prefix + f"- {note}\n".encode("utf-8"))
    except OSError as exc:
        parser.error(str(exc))
    print(path.resolve())


if __name__ == "__main__":
    main()
