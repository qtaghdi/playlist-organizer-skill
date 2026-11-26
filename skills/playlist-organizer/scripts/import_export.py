#!/usr/bin/env python3
"""Convert a user-provided Spotify or YouTube playlist export to portable CSV."""

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys

FIELDS = ("title", "artist", "track_id", "playlist", "playlist_id", "album", "last_played", "play_count")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def spotify_history(paths, selected_ids, minimum_ms):
    counts, latest = Counter(), {}
    for path in dict.fromkeys(p.resolve() for p in paths):
        records = read_json(path)
        if not isinstance(records, list) or any(not isinstance(row, dict) for row in records):
            raise ValueError(f"{path.name} must contain an array of Extended Streaming History records")
        if records and not any("spotify_track_uri" in row for row in records):
            raise ValueError(f"{path.name} has no spotify_track_uri field")
        for row in records:
            track_id = row.get("spotify_track_uri")
            played = row.get("ms_played")
            if track_id not in selected_ids or type(played) is not int or played < minimum_ms or not row.get("ts"):
                continue
            stamp = datetime.fromisoformat(row["ts"].replace("Z", "+00:00"))
            if stamp.tzinfo is None:
                stamp = stamp.replace(tzinfo=timezone.utc)
            counts[track_id] += 1
            if track_id not in latest or stamp > latest[track_id]:
                latest[track_id] = stamp
    return counts, latest


def spotify_rows(args):
    export = read_json(args.input)
    if not isinstance(export, dict) or not isinstance(export.get("playlists"), list):
        raise ValueError("Spotify Account Data input must contain a playlists array")
    selectors = set(args.playlist)
    found, rows = set(), []
    skipped = empty = 0
    for number, playlist in enumerate(export["playlists"], start=1):
        if not isinstance(playlist, dict) or not isinstance(playlist.get("name"), str):
            raise ValueError(f"Spotify playlist {number} is missing its name")
        name = playlist["name"].strip()
        if selectors and name not in selectors:
            continue
        found.add(name)
        items = playlist.get("items")
        if not isinstance(items, list):
            raise ValueError(f"Spotify playlist {number} is missing its items array")
        start = len(rows)
        for item in items:
            if not isinstance(item, dict):
                raise ValueError(f"Spotify playlist {number} contains an invalid item")
            track = item.get("track") or item.get("localTrack")
            if isinstance(track, str) and track.strip():
                track = {"trackName": track.strip()}
            if not isinstance(track, dict) or not track.get("trackName"):
                skipped += 1
                continue
            uri = track.get("trackUri", "")
            rows.append({
                "title": track["trackName"], "artist": track.get("artistName", ""),
                "track_id": uri if isinstance(uri, str) and uri.startswith("spotify:track:") else "",
                "playlist": name, "playlist_id": f"spotify-export-{args.input.stem}-{number}",
                "album": track.get("albumName", ""),
            })
        empty += len(rows) == start
    if selectors - found:
        raise ValueError("One or more selected Spotify playlist names were absent from the export")
    if args.history:
        counts, latest = spotify_history(args.history, {row["track_id"] for row in rows if row["track_id"]}, args.min_ms)
        for row in rows:
            uri = row["track_id"]
            if uri in latest:
                row.update(last_played=latest[uri].astimezone(timezone.utc).isoformat(), play_count=counts[uri])
        print(f"History joined to {len(latest)} tracks by exact URI.", file=sys.stderr)
    print(f"Skipped {skipped} unavailable or non-song entries. {empty} selected playlists have no usable rows.",
          file=sys.stderr)
    return rows


def read_metadata(path):
    if path is None:
        return {}
    result = {}
    with path.open(encoding="utf-8-sig", newline="") as source:
        rows = csv.DictReader(source)
        if not {"track_id", "title"}.issubset(rows.fieldnames or []):
            raise ValueError("YouTube metadata CSV requires track_id and title columns")
        for row in rows:
            key = (row.get("track_id") or "").strip()
            title = (row.get("title") or "").strip()
            if key and title:
                values = {field: (row.get(field) or "").strip() for field in ("title", "artist", "album")}
                if key in result and values != result[key]:
                    raise ValueError(f"conflicting metadata for video ID {key}")
                result[key] = values
    return result


def youtube_rows(args):
    lookup = read_metadata(args.metadata)
    name = args.playlist or args.input.stem
    playlist_id = args.playlist_id or args.input.stem
    with args.input.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.reader(source)
        for header in reader:
            fields = [re.sub(r"[^a-z0-9]", "", key.lower()) for key in header]
            if "videoid" in fields:
                break
        else:
            raise ValueError("YouTube export needs a Video ID column in its track section")
        column = fields.index("videoid")
        rows, unknown = [], 0
        for line in reader:
            if not any(cell.strip() for cell in line):
                continue
            if column >= len(line) or not re.fullmatch(r"[A-Za-z0-9_-]+", line[column].strip()):
                raise ValueError(f"invalid video ID on CSV line {reader.line_num}")
            identity = line[column].strip()
            metadata = lookup.get(identity, {})
            unknown += not metadata
            rows.append({
                "title": metadata.get("title", f"[Video {identity}]"),
                "artist": metadata.get("artist", ""), "album": metadata.get("album", ""),
                "track_id": identity, "playlist": name, "playlist_id": playlist_id,
            })
    print(f"{unknown} of {len(rows)} occurrences have video IDs only. Add track metadata before grouping those songs.",
          file=sys.stderr)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="service", required=True)
    spotify = subcommands.add_parser("spotify", help="Spotify Account Data playlist JSON")
    spotify.add_argument("input", type=Path)
    spotify.add_argument("--playlist", action="append", default=[], help="exact playlist name (repeatable)")
    spotify.add_argument("--history", action="append", default=[], type=Path,
                         help="optional, non-overlapping Extended Streaming History JSON (repeatable)")
    spotify.add_argument("--min-ms", type=int, default=30000, help="minimum time to count a play (default 30000)")
    youtube = subcommands.add_parser("youtube", help="YouTube or YouTube Music Takeout playlist CSV")
    youtube.add_argument("input", type=Path)
    youtube.add_argument("--playlist", help="playlist name (default input filename stem)")
    youtube.add_argument("--playlist-id", help="source playlist ID (default input filename stem)")
    youtube.add_argument("--metadata", type=Path, help="optional metadata CSV keyed by video ID")
    args = parser.parse_args()
    if args.service == "spotify" and args.min_ms < 0:
        parser.error("--min-ms must be nonnegative")
    try:
        rows = spotify_rows(args) if args.service == "spotify" else youtube_rows(args)
    except (OSError, TypeError, ValueError, csv.Error) as exc:
        parser.error(str(exc))
    out = csv.DictWriter(sys.stdout, fieldnames=FIELDS)
    out.writeheader()
    out.writerows(rows)


if __name__ == "__main__":
    main()
