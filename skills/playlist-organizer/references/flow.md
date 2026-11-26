# Review and sequence a playlist

## Decide what should feel continuous

Identify whether the user normally shuffles, starts from the first track, or expects continuous listening. Use existing playlists and familiar favorites to find anchors. Use confirmed attributes such as arrangement, vocal prominence, rhythm, energy, and transition behavior when available. Genre and co-membership suggest broad relationships. Play counts help choose familiar anchors. Keep inferred texture or energy separate from listening observations and measured tempo.

Review membership and sequence in separate passes.

- **Membership.** Identify the sound or purpose that holds a playlist together. Scan for records that share a catalog genre but serve a different purpose, such as a vocal soundtrack single in a quiet instrumental set. Rehome clear outliers where they fit. Keep distinct recordings and edits when requested or when nothing justifies removing them.
- **Sequence.** Choose a few representative opening tracks. Look at the opening, closing, and short runs across longer lists. Use a shared texture or moderate change in energy between groups. Spread versions of the same song and avoid unnecessary blocks of one performer. Preserve deliberate runs and repeated entries. Consider different sounds within a large playlist when the user wants variety.
- **Replacement order.** Reinsert a verified replacement at the original occurrence in the plan. Review the neighborhood again if the version changes duration, arrangement, or intensity. Compare the applied sequence with the plan, especially when the service adds tracks at the end.

Explain the most consequential edits with concrete track examples. If playback was unavailable, identify the source of the judgment, such as the track list and the user's existing groupings.

## Verify the applied sequence

For live edits, keep a fresh before snapshot. Verify playlist IDs, membership and order after applying the plan. When rehoming tracks without pruning, compare the combined track multiset across the affected playlists. A correct count alone can hide missing entries, duplicate entries, and songs appended out of order. Check unaffected playlists and favorites when the operations might touch them.

Use the read-only checker with an inventory from `audit.py`. Use stable track IDs from the audit's `persistent_id` field. For CSV, provide `track_id` for all occurrences and keep playlist IDs consistent between files.

The expected-order file is a JSON object keyed by playlist ID. Its values are the intended track IDs in order, including any repeated occurrences.

```json
{
  "PLAYLIST_ID": ["TRACK_A", "TRACK_B", "TRACK_A", "TRACK_C"]
}
```

From the skill directory, select the relevant playlists in a fresh export and write the inventory locally.

```sh
python3 scripts/audit.py /path/to/after.xml --playlist PLAYLIST_ID --signals order --tracks > after.json
python3 scripts/verify_order.py plan.json after.json
```

Read the first mismatched position and missing or extra occurrences before retrying. When only positions differ, fix the order if the client supports it and the edit is authorized. Report any remaining order difference.
