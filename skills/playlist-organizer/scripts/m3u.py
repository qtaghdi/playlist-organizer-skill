#!/usr/bin/env python3
"""Read a music playlist into portable CSV or write its new order to an M3U file."""

import argparse
from collections import defaultdict, deque
import csv
import hashlib
import json
import ntpath
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


def is_url(locator):
    return re.match(r"^[a-z][a-z0-9+.-]*://", locator, re.IGNORECASE) is not None


def is_absolute(locator):
    return os.path.isabs(locator) or ntpath.isabs(locator)


def identity(locator, folder):
    if is_url(locator) or (ntpath.isabs(locator) and not os.path.isabs(locator)):
        key = locator
    else:
        key = os.path.normcase(os.path.abspath(folder.resolve() / locator))
    return "m3u:" + hashlib.sha256(key.encode("utf-8")).hexdigest()


def read_playlist(path, encoding):
    header, entries, pending = [], [], []
    for line in path.read_text(encoding=encoding).splitlines():
        if not line.strip() or line.upper() == "#EXTM3U":
            continue
        if line.upper().startswith("#EXT-X-"):
            raise ValueError("HLS manifests are not supported music playlists")
        if not entries and line.upper().startswith("#PLAYLIST:"):
            header.append(line)
        elif line.startswith("#"):
            pending.append(line)
        else:
            entries.append((identity(line, path.parent), pending, line))
            pending = []
    if any(line.upper().startswith("#EXTINF:") for line in pending):
        raise ValueError("playlist ends with an EXTINF entry that has no track locator")
    return header, entries, pending


def labels(details, locator):
    label = next((line.partition(",")[2].strip() for line in details
                  if line.upper().startswith("#EXTINF:") and "," in line), "")
    if " - " in label:
        artist, _, title = label.partition(" - ")
        if artist.strip() and title.strip():
            return title.strip(), artist.strip()
    if label:
        return label, ""
    path = unquote(urlsplit(locator).path) if is_url(locator) else locator
    basename = ntpath.basename(path.rstrip("/\\"))
    return ntpath.splitext(basename)[0] or "[Unlabeled track]", ""


def write_csv(source, entries, name):
    writer = csv.writer(sys.stdout)
    writer.writerow(("title", "artist", "track_id", "playlist", "playlist_id"))
    canonical_labels = {}
    for track_id, details, locator in entries:
        title, artist = canonical_labels.setdefault(track_id, labels(details, locator))
        writer.writerow((title, artist, track_id, name, source.stem))


def rebase(locator, source, destination):
    if source.parent.resolve() == destination.parent.resolve() or is_url(locator) or is_absolute(locator):
        return locator
    if ntpath.splitdrive(locator)[0]:
        raise ValueError("cannot rebase a drive-relative path to a different folder")
    relative = os.path.relpath(source.parent.resolve() / locator, destination.parent.resolve())
    return "." + os.sep + relative if relative.startswith("#") else relative


def render(source, destination, header, entries, tail, order):
    if not isinstance(order, list) or not all(isinstance(item, str) for item in order):
        raise ValueError("order must be a JSON array of track IDs")
    available = defaultdict(deque)
    for track_id, details, locator in entries:
        available[track_id].append((details, locator))
    lines = ["#EXTM3U", *header]
    for track_id in order:
        if not available[track_id]:
            raise ValueError(f"unknown track ID or too many occurrences of {track_id}")
        details, locator = available[track_id].popleft()
        lines.extend(details)
        lines.append(rebase(locator, source, destination))
    return "\n".join([*lines, *tail]) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="action", required=True)
    for name in ("read", "write"):
        sub = subcommands.add_parser(name)
        sub.add_argument("source", type=Path, help="local M3U or M3U8 playlist")
        sub.add_argument("--encoding", default="utf-8-sig", help="source encoding (default UTF-8 with optional BOM)")
        if name == "read":
            sub.add_argument("--playlist", help="playlist name (default source filename stem)")
        else:
            sub.add_argument("order", type=Path, help="JSON array of ordered track IDs")
            sub.add_argument("output", type=Path, help="new M3U or M3U8 file")
    args = parser.parse_args()
    try:
        header, entries, tail = read_playlist(args.source, args.encoding)
        if args.action == "read":
            write_csv(args.source, entries, args.playlist or args.source.stem)
        else:
            order = json.loads(args.order.read_text(encoding="utf-8"))
            content = render(args.source, args.output, header, entries, tail, order)
            with args.output.open("x", encoding="utf-8", newline="\n") as output:
                output.write(content)
    except (OSError, LookupError, ValueError, csv.Error) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
