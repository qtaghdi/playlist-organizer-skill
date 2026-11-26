# Last.fm and ListenBrainz history

Use listening history as a separate input. It can cover several music apps. Ask which source and period the user wants to use. Keep gaps and playback before the available range unknown.

`scripts/join_history.py` reads local JSON. Save the necessary Last.fm `user.getRecentTracks` response pages with dates. For ListenBrainz, prefer the account history export ZIP. The tool also accepts extracted monthly JSONL, a limited `payload.listens` response, and JSON arrays. Use the official API or a user-provided export. Save only the account and pages the user authorized. Keep API keys out of files and chat.

Start with a [portable playlist CSV](portable-inputs.md). Add `track_id` where available and an optional `recording_mbid` column for MusicBrainz recording IDs, especially when joining Last.fm data. ListenBrainz can also provide Spotify track URIs and YouTube video IDs. Missing identifiers can be matched by exact title and artist with `--allow-title-match`, but only where the match is unambiguous. An automatically suggested MusicBrainz mapping alone does not establish an exact recording match. Keep live, remastered, and other distinctly labeled recordings separate.

```sh
python3 scripts/join_history.py lastfm mix.csv lastfm-page1.json lastfm-page2.json > with-history.csv
python3 scripts/join_history.py listenbrainz mix.csv listens.zip --allow-title-match > with-history.csv
python3 scripts/audit.py with-history.csv --library --signals recency,plays --tracks
```

The output holds the latest matched timestamp and the number of distinct timestamps for each matched song in the supplied history. Counts are scoped to the loaded files. The tool ignores now-playing entries without completed timestamps and avoids double-counting overlapping entries. It keeps existing play statistics unless `--replace-history` is requested. Keep other history sources separate if their time ranges overlap.

- [Last.fm user.getRecentTracks](https://www.last.fm/api/show/user.getRecentTracks)
- [ListenBrainz history export](https://listenbrainz.readthedocs.io/en/latest/users/api/export.html)
- [ListenBrainz listens endpoint](https://listenbrainz.readthedocs.io/en/latest/users/api/core.html)
