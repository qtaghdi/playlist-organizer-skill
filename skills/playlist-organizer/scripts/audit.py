#!/usr/bin/env python3
"""Inventory a playlist CSV or Apple Music XML export without changing the source."""

import argparse
from collections import Counter
import csv
from datetime import date, datetime, timezone
import json
import plistlib
from pathlib import Path
from xml.parsers.expat import ExpatError
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

SIGNALS = {
    "edition": ("Album", "Album Artist", "Disc Number", "Track Number", "Total Time", "Release Date"),
    "favorites": ("Favorited", "Loved", "Disliked", "Rating"),
    "genre": ("Genre",),
    "order": (),
    "plays": ("Play Count",),
    "recency": ("Play Date UTC", "Date Added"),
    "skips": ("Skip Count", "Skip Date"),
    "tempo": ("BPM",),
    "versions": (),
}


def load_csv(path, zone):
    """Map the portable CSV fields to the track and playlist inventory."""
    tracks = {}
    ids = {}
    playlists = {}
    with path.open(encoding="utf-8-sig", newline="") as source:
        rows = csv.DictReader(source)
        if not {"title", "artist"}.issubset(rows.fieldnames or []):
            raise ValueError("CSV requires title and artist columns")
        for line, record in enumerate(rows, start=2):
            if None in record or None in record.values():
                raise ValueError(f"CSV row {line} has the wrong number of fields")
            row = {key: value.strip() for key, value in record.items()}
            if not any(row.values()):
                continue
            if not row["title"]:
                raise ValueError(f"CSV row {line} has no title")

            key = row.get("track_id")
            track_id = ids.get(key, line)
            track = {"Track ID": track_id, "Name": row["title"], "Artist": row["artist"]}
            if key:
                ids[key] = track_id
                track["Persistent ID"] = key
            for key, field in (("album", "Album"), ("genre", "Genre")):
                if row.get(key):
                    track[field] = row[key]
            for key, field in (("play_count", "Play Count"), ("skip_count", "Skip Count"), ("bpm", "BPM")):
                if row.get(key):
                    try:
                        track[field] = int(row[key])
                        if track[field] < 0:
                            raise ValueError()
                    except ValueError as exc:
                        raise ValueError(f"CSV row {line} has invalid {key}") from exc
            for key, field in (("last_played", "Play Date UTC"), ("date_added", "Date Added"), ("last_skipped", "Skip Date")):
                if row.get(key):
                    try:
                        value = datetime.fromisoformat(row[key].replace("Z", "+00:00"))
                    except ValueError as exc:
                        raise ValueError(f"CSV row {line} has invalid {key}") from exc
                    track[field] = value if value.tzinfo is not None else value.replace(tzinfo=zone)
            if row.get("favorite"):
                value = row["favorite"].lower()
                if value not in ("true", "false", "1", "0"):
                    raise ValueError(f"CSV row {line} has invalid favorite")
                track["Favorited"] = value in ("true", "1")
            if row.get("version"):
                value = row["version"].lower()
                if value not in ("clean", "explicit", "unmarked"):
                    raise ValueError(f"CSV row {line} has invalid version")
                track["Clean"] = value == "clean"
                track["Explicit"] = value == "explicit"

            existing = tracks.setdefault(track_id, {})
            if any(field in existing and existing[field] != value for field, value in track.items()):
                raise ValueError(f"CSV row {line} conflicts with prior metadata for the same track_id")
            existing.update(track)

            name, source_id = row.get("playlist"), row.get("playlist_id")
            if name or source_id:
                playlist_key = ("id", source_id) if source_id else ("name", name)
                playlist = playlists.setdefault(playlist_key, {
                    "Playlist Persistent ID": str(len(playlists) + 1),
                    "Name": name or None,
                    "Playlist Items": [],
                })
                if name and playlist["Name"] not in (None, name):
                    raise ValueError(f"CSV row {line} conflicts with a prior playlist title")
                if name:
                    playlist["Name"] = name
                playlist["Playlist Items"].append({"Track ID": track_id})
    for (_, key), playlist in playlists.items():
        if playlist["Name"] is None:
            playlist["Name"] = key
    return {"Tracks": tracks, "Playlists": list(playlists.values())}


def music_date(value, zone):
    if not isinstance(value, datetime):
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(zone).date()


def playlist_id(playlist):
    return playlist.get("Playlist Persistent ID") or str(playlist["Playlist ID"])


def members(playlist):
    return [item["Track ID"] for item in playlist.get("Playlist Items", [])]


def playlist_kind(playlist):
    if playlist.get("Folder"):
        return "folder"
    if playlist.get("Master") or "Distinguished Kind" in playlist:
        return "system"
    if "Smart Info" in playlist or "Smart Criteria" in playlist:
        return "smart"
    return "unverified"


def favorite(track):
    return bool(track.get("Favorited") or track.get("Loved"))


def version(track):
    clean, explicit = track.get("Clean"), track.get("Explicit")
    if clean and explicit:
        return "conflicting"
    if clean:
        return "clean"
    if explicit:
        return "explicit"
    return "unmarked"


def recency(track, args, zone):
    last_play = music_date(track.get("Play Date UTC"), zone)
    added = music_date(track.get("Date Added"), zone)
    if last_play is not None and last_play > args.cutoff:
        return "recent"
    if args.protect_favorites and favorite(track):
        return "protected_favorite"
    if args.recent_additions == "protect" and added is not None and added > args.cutoff:
        return "recently_added"
    if last_play is not None:
        return "stale"
    if args.unknown == "flag-old-additions" and added is not None and added <= args.cutoff:
        return "review_unknown_old_addition"
    return "unknown"


def projected_track(track, signals, status, memberships, zone):
    projected = {
        "track_id": track["Track ID"],
        "persistent_id": track.get("Persistent ID"),
        "title": track.get("Name"),
        "artist": track.get("Artist"),
        "playlist_only": bool(track.get("Playlist Only")),
    }
    if status is not None:
        projected["recency"] = status
    if "versions" in signals:
        projected["version"] = version(track)
    if memberships:
        projected["playlist_ids"] = list(memberships)
    if "order" in signals:
        projected["positions"] = memberships
    for signal in sorted(signals):
        for field in SIGNALS[signal]:
            value = track.get(field)
            if field == "Release Date" and isinstance(value, datetime):
                value = value.date().isoformat()
            elif isinstance(value, datetime):
                value = music_date(value, zone).isoformat()
            if value is not None:
                projected[field] = value
    return projected


def audit(export, args, signals, zone):
    playlists = export["Playlists"]
    tracks = {track["Track ID"]: track for track in export["Tracks"].values()}
    by_id = {playlist_id(playlist): playlist for playlist in playlists}
    if len(by_id) != len(playlists):
        raise ValueError("duplicate playlist IDs in export")
    if len(tracks) != len(export["Tracks"]):
        raise ValueError("duplicate track IDs in export")

    if args.library:
        ids = {track_id for track_id, track in tracks.items() if not track.get("Playlist Only")}
    else:
        ids = {track_id for pid in args.playlist for track_id in members(by_id[pid])}

    positions = {}
    listing = []
    for pid, playlist in by_id.items():
        entries = members(playlist)
        listing.append({
            "id": pid,
            "title": playlist.get("Name"),
            "parent_id": playlist.get("Parent Persistent ID"),
            "kind": playlist_kind(playlist),
            "entry_count": len(entries),
        })
        if pid in args.playlist or (args.library and "order" in signals):
            for position, track_id in enumerate(entries, start=1):
                positions.setdefault(track_id, {}).setdefault(pid, []).append(position)

    selected = [tracks[track_id] for track_id in sorted(ids & tracks.keys())]
    statuses = {
        track["Track ID"]: recency(track, args, zone)
        for track in selected
    } if args.cutoff is not None else {}
    summary = {
        "unique_tracks": len(selected),
        "playlist_only": sum(bool(track.get("Playlist Only")) for track in selected),
        "unresolved_track_ids": sorted(ids - tracks.keys()),
    }
    if "recency" in signals:
        summary["last_played_available"] = sum(isinstance(track.get("Play Date UTC"), datetime) for track in selected)
        summary["date_added_available"] = sum(isinstance(track.get("Date Added"), datetime) for track in selected)
    if statuses:
        summary["recency"] = dict(Counter(statuses.values()))
    if "genre" in signals:
        summary["genres"] = dict(Counter(track.get("Genre") or "Unspecified" for track in selected).most_common(12))
    if "favorites" in signals:
        summary["marked_favorite"] = sum(map(favorite, selected))
    if "versions" in signals:
        summary["versions"] = dict(Counter(map(version, selected)))

    output = {
        "playlists": listing,
        "scope": "library" if args.library else list(dict.fromkeys(args.playlist)),
        "signals": sorted(signals),
        "timezone": args.timezone,
        "cutoff_inclusive": args.cutoff.isoformat() if args.cutoff else None,
        "protect_favorites": args.protect_favorites,
        "recent_additions": args.recent_additions,
        "unknown_policy": args.unknown,
        "summary": summary,
    }
    if args.tracks:
        output["tracks"] = [
            projected_track(track, signals, statuses.get(track["Track ID"]), positions.get(track["Track ID"], {}), zone)
            for track in selected
        ]
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", type=Path, help="local CSV or Apple Music XML export")
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--library", action="store_true", help="select all CSV tracks or the library in a full XML export")
    scope.add_argument("--playlist", action="append", default=[], help="playlist ID reported by the inventory (repeatable)")
    parser.add_argument("--signals", default="", help="comma-separated fields: " + ", ".join(SIGNALS))
    parser.add_argument("--tracks", action="store_true", help="include individual tracks in the report")
    parser.add_argument("--cutoff", type=date.fromisoformat, help="inclusive local cutoff date (YYYY-MM-DD)")
    parser.add_argument("--timezone", default="UTC", help="IANA timezone for play and add dates (default UTC)")
    parser.add_argument("--protect-favorites", action="store_true", help="protect marked favorites from stale flags")
    parser.add_argument("--recent-additions", choices=["protect", "consider"], default="protect",
                        help="whether to protect tracks added after the cutoff")
    parser.add_argument("--unknown", choices=["keep", "flag-old-additions"], default="keep",
                        help="how to label tracks without a last-played date")
    args = parser.parse_args()

    signals = {signal.strip() for signal in args.signals.split(",") if signal.strip()}
    if signals - SIGNALS.keys():
        parser.error("unknown signals: " + ", ".join(sorted(signals - SIGNALS.keys())))
    if args.cutoff is not None and "recency" not in signals:
        parser.error("--cutoff requires the recency signal")
    if args.protect_favorites and ("favorites" not in signals or args.cutoff is None):
        parser.error("--protect-favorites requires the favorites signal and --cutoff")
    if args.unknown != "keep" and args.cutoff is None:
        parser.error("--unknown flag-old-additions requires --cutoff")
    if args.recent_additions != "protect" and args.cutoff is None:
        parser.error("--recent-additions consider requires --cutoff")
    if (signals or args.tracks) and not (args.library or args.playlist):
        parser.error("select --library or --playlist to analyze tracks")

    try:
        zone = ZoneInfo(args.timezone)
        if args.export.suffix.lower() == ".csv":
            export = load_csv(args.export, zone)
        else:
            with args.export.open("rb") as source:
                export = plistlib.load(source)
        result = audit(export, args, signals, zone)
    except ZoneInfoNotFoundError:
        parser.error(f"unknown timezone: {args.timezone}")
    except KeyError as exc:
        parser.error(f"playlist ID or export field missing: {exc}")
    except (OSError, ValueError, plistlib.InvalidFileException, TypeError, ExpatError) as exc:
        parser.error(f"could not read export: {exc}")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
