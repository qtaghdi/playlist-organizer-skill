# Portable playlist inputs

Use a local CSV file or a user-provided track list when the service does not supply an editable connection. Convert custom exports to the CSV format only where the source fields have matching meaning. Avoid filling gaps with invented metadata. A plain track list still supports grouping, title ideas, and draft ordering.

## CSV format

Use UTF-8 and include `title` and `artist` columns. Each record represents one track occurrence. Use `playlist` for the list name and add `playlist_id` to distinguish lists with the same name. File row order determines playlist order.

When a stable service ID is available, include it in `track_id`. Repeat it when the same catalog edition appears in multiple playlists. Rows without a track ID are treated as distinct. Fields for the same ID must agree when present. Keep live or alternate releases under their own IDs.

Optional fields are `album`, `genre`, `last_played`, `date_added`, `play_count`, `skip_count`, `last_skipped`, `favorite`, `bpm`, and `version`. Leave unknown fields blank. Use ISO dates or timestamps; dates and timestamps without offsets use the selected timezone. Favorites accept `true`, `false`, `1`, and `0`. Version values are `clean`, `explicit`, and `unmarked`.

```csv
title,artist,track_id,playlist,last_played,favorite
Harbor Lights,Example Artist,demo-1,Evening,2026-04-20,true
Day Trip,Another Artist,demo-2,Morning,2026-05-04,false
Harbor Lights,Example Artist,demo-1,Weekend,2026-04-20,true
```

From the skill directory:

```sh
python3 scripts/audit.py /path/to/playlists.csv
python3 scripts/audit.py /path/to/playlists.csv --playlist 1 --signals recency,order,favorites --tracks
python3 scripts/audit.py /path/to/playlists.csv --library --signals recency --cutoff 2026-03-01 --timezone UTC
```

Use the IDs printed by the first command to select lists. These playlist IDs and numeric track IDs are local to that export. When presenting a plan for application, include the service's identifiers when available. For a CSV, `--library` simply selects all records in the supplied file.

The audit is read-only. For live edits, use a supported integration or the service's controls, verify permissions and available operations, then check the result. A missing feature or absent field may limit an edit such as transferring a favorite. When the service is unavailable, provide scoped track lists and a change plan for that service.
