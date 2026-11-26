#!/usr/bin/env python3
"""Compare a playlist order plan with audit.py output."""

import argparse
from collections import Counter
import json
from pathlib import Path


def observed_order(playlist, tracks):
    playlist_id = playlist["id"]
    count = playlist["entry_count"]
    entries = [None] * count
    for track in tracks:
        positions = track.get("positions", {}).get(playlist_id, [])
        if not positions:
            continue
        identity = track.get("persistent_id")
        if not isinstance(identity, str) or not identity:
            raise ValueError(f"{playlist_id} has a track without a persistent ID")
        for position in positions:
            if not isinstance(position, int) or not 1 <= position <= count or entries[position - 1] is not None:
                raise ValueError(f"{playlist_id} has an invalid or duplicate position {position}")
            entries[position - 1] = identity
    if None in entries:
        raise ValueError(f"{playlist_id} has incomplete positions. Select it and use --signals order --tracks.")
    return entries


def compare(plan, inventory):
    if not isinstance(plan, dict) or not plan:
        raise ValueError("plan must be a nonempty JSON object of playlist IDs and ordered track IDs")
    if "order" not in inventory["signals"] or "tracks" not in inventory:
        raise ValueError("inventory requires --signals order --tracks")
    scope = inventory["scope"]
    playlists = {p["id"]: p for p in inventory["playlists"]}
    result = {}
    for playlist_id, expected in plan.items():
        if not isinstance(expected, list) or not all(isinstance(i, str) and i for i in expected):
            raise ValueError(f"{playlist_id} needs an ordered list of persistent track IDs")
        if scope != "library" and playlist_id not in scope:
            raise ValueError(f"{playlist_id} was not selected for the inventory")
        actual = observed_order(playlists[playlist_id], inventory["tracks"])
        mismatch = next((index for index, pair in enumerate(zip(expected, actual), start=1) if pair[0] != pair[1]), None)
        if mismatch is None and len(expected) != len(actual):
            mismatch = min(len(expected), len(actual)) + 1
        expected_counts, actual_counts = Counter(expected), Counter(actual)
        result[playlist_id] = {
            "expected_count": len(expected),
            "actual_count": len(actual),
            "first_mismatch_at": mismatch,
            "missing_occurrences": dict(expected_counts - actual_counts),
            "extra_occurrences": dict(actual_counts - expected_counts),
        }
    return {"ok": all(p["first_mismatch_at"] is None for p in result.values()), "playlists": result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="JSON mapping playlist IDs to ordered persistent track IDs")
    parser.add_argument("inventory", type=Path, help="audit.py JSON output with track positions")
    args = parser.parse_args()
    try:
        result = compare(json.loads(args.plan.read_text(encoding="utf-8")),
                         json.loads(args.inventory.read_text(encoding="utf-8")))
    except (OSError, TypeError, ValueError, KeyError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
