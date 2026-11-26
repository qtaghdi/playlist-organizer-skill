#!/usr/bin/env python3
"""Add Last.fm or ListenBrainz plays from local JSON to a portable playlist CSV."""

import argparse
from collections import defaultdict
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import parse_qs, urlsplit
from zipfile import BadZipFile, ZipFile


def clean(value):
    return value.strip() if isinstance(value, str) else ""


def name_key(title, artist):
    return tuple(unicodedata.normalize("NFC", clean(s)).casefold() for s in (title, artist))


def track_key(value):
    value = clean(value)
    if "://" not in value:
        return value
    url = urlsplit(value)
    if url.hostname == "open.spotify.com" and "/track/" in url.path:
        return "spotify:track:" + url.path.rstrip("/").rsplit("/", 1)[-1]
    if url.hostname in {"www.youtube.com", "music.youtube.com", "youtube.com"}:
        return parse_qs(url.query).get("v", [""])[0]
    if url.hostname == "youtu.be":
        return url.path.lstrip("/")
    return value


def mbid(value):
    value = clean(value).lower()
    return value if re.fullmatch(r"[\da-f]{8}(?:-[\da-f]{4}){3}-[\da-f]{12}", value) else ""


def history_rows(path, provider):
    if provider == "listenbrainz" and path.suffix.lower() == ".zip":
        with ZipFile(path) as archive:
            members = [name for name in archive.namelist() if re.fullmatch(r"listens/\d{4}/\d{1,2}\.jsonl", name)]
            if not members:
                raise ValueError(f"{path.name} has no ListenBrainz monthly listens files")
            for member in members:
                with archive.open(member) as lines:
                    yield from (json.loads(line.decode("utf-8-sig")) for line in lines if line.strip())
        return
    if provider == "listenbrainz" and path.suffix.lower() == ".jsonl":
        with path.open(encoding="utf-8-sig") as lines:
            yield from (json.loads(line) for line in lines if line.strip())
        return
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if provider == "lastfm":
        entries = data.get("recenttracks", {}).get("track") if isinstance(data, dict) else None
    else:
        entries = data if isinstance(data, list) else data.get("payload", {}).get("listens") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        raise ValueError(f"{path.name} does not contain a {provider} history list")
    yield from entries


def read_events(path, provider):
    for entry in history_rows(path, provider):
        if not isinstance(entry, dict):
            raise ValueError(f"{path.name} contains an invalid history entry")
        if provider == "lastfm":
            artist = entry.get("artist") or {}
            timestamp = (entry.get("date") or {}).get("uts")
            title = entry.get("name")
            recording = mbid(entry.get("mbid"))
            identities = []
            artist = artist.get("#text") or artist.get("name") if isinstance(artist, dict) else artist
        else:
            track = entry.get("track_metadata") or {}
            extra = track.get("additional_info") or {}
            timestamp = entry.get("listened_at")
            title, artist = track.get("track_name"), track.get("artist_name")
            recording = mbid(extra.get("recording_mbid"))
            identities = [track_key(extra.get(k)) for k in ("spotify_id", "origin_url", "youtube_id")]
        if isinstance(timestamp, bool) or not timestamp or not str(timestamp).isascii() or not str(timestamp).isdigit():
            continue
        yield int(timestamp), {key for key in identities if key}, recording, name_key(title, artist)


def join(rows, events, title_match, replace):
    tracks, recordings, names = defaultdict(set), defaultdict(set), defaultdict(set)
    row_keys = []
    for index, row in enumerate(rows):
        track_id = track_key(row.get("track_id"))
        recording_id = mbid(row.get("recording_mbid"))
        key = ("track", track_id) if track_id else ("recording", recording_id) if recording_id else ("row", index)
        row_keys.append(key)
        if track_id:
            tracks[track_id].add(key)
        if recording_id:
            recordings[recording_id].add(key)
        name = name_key(row.get("title"), row.get("artist"))
        if all(name):
            names[name].add(key)

    defined_recordings = defaultdict(set)
    for row, key in zip(rows, row_keys):
        recording_id = mbid(row.get("recording_mbid"))
        if recording_id:
            defined_recordings[key].add(recording_id)
    matches = defaultdict(set)
    seen = set()
    unresolved = 0
    for timestamp, identities, recording, name in events:
        signature = timestamp, tuple(sorted(identities)), recording, name
        if signature in seen:
            continue
        seen.add(signature)
        exact_tracks = set().union(*(tracks[key] for key in identities))
        exact_recordings = recordings[recording] if recording else set()
        if exact_tracks and exact_recordings:
            candidates = exact_tracks & exact_recordings
        elif exact_tracks or exact_recordings:
            candidates = exact_tracks or exact_recordings
        elif title_match and all(name):
            candidates = names[name]
        else:
            candidates = set()
        candidates = {key for key in candidates
                      if not (recording and defined_recordings[key] and recording not in defined_recordings[key])}
        if len(candidates) != 1:
            unresolved += 1
            continue
        matches[next(iter(candidates))].add(timestamp)

    existing = {key for row, key in zip(rows, row_keys) if row.get("last_played") or row.get("play_count")}
    updated = set()
    for row, key in zip(rows, row_keys):
        timestamps = matches.get(key)
        if timestamps and (replace or key not in existing):
            row["last_played"] = datetime.fromtimestamp(max(timestamps), timezone.utc).isoformat()
            row["play_count"] = len(timestamps)
            updated.add(key)
    return len(matches), len(updated), unresolved


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("provider", choices=("lastfm", "listenbrainz"))
    parser.add_argument("playlist", type=Path, help="portable playlist CSV")
    parser.add_argument("history", nargs="+", type=Path, help="local history JSON, ListenBrainz JSONL, or an export ZIP")
    parser.add_argument("--allow-title-match", action="store_true", help="allow unambiguous title and artist matches")
    parser.add_argument("--replace-history", action="store_true", help="replace existing history only for matched songs")
    args = parser.parse_args()
    try:
        with args.playlist.open(encoding="utf-8-sig", newline="") as source:
            reader = csv.DictReader(source)
            fields = list(reader.fieldnames or [])
            if not {"title", "artist"}.issubset(fields) or len(fields) != len(set(fields)):
                raise ValueError("playlist CSV needs unique columns including title and artist")
            rows = list(reader)
            if any(None in row or None in row.values() for row in rows):
                raise ValueError("playlist CSV contains a row with the wrong number of columns")
        files = dict.fromkeys(path.resolve() for path in args.history)
        events = (event for path in files for event in read_events(path, args.provider))
        matched, updated, unresolved = join(rows, events, args.allow_title_match, args.replace_history)
        fields.extend(field for field in ("last_played", "play_count") if field not in fields)
        writer = csv.DictWriter(sys.stdout, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    except (OSError, TypeError, ValueError, AttributeError, OverflowError, csv.Error, BadZipFile) as exc:
        parser.error(str(exc))
    print(f"Matched {matched} songs. Updated {updated}. Unmatched or ambiguous plays: {unresolved}.", file=sys.stderr)


if __name__ == "__main__":
    main()
