# M3U and M3U8 files

Read a local playlist into a portable CSV. The tool keeps the original order and repeated entries. It uses EXTINF labels when present and filenames as a fallback. Opaque track IDs let you plan an order without exposing the original paths or URLs in the CSV. Filename labels can still reveal personal information, so review the output before sharing it.

```sh
python3 scripts/m3u.py read "My Mix.m3u8" > mix.csv
```

Write a JSON array of the retained track IDs in their intended order, including repeated IDs where wanted. Use that array to create a new playlist from the original. The tool preserves the matching per-track metadata and locators, rebases relative paths when saving to another directory, and refuses to overwrite an existing file. It reads UTF-8 by default and accepts `--encoding` for older source files. It does not load or check remote media.

```sh
python3 scripts/m3u.py write "My Mix.m3u8" order.json "My Mix revised.m3u8"
```

Read the result again to check track IDs and sequence, then open it in the user's player if available. File playlists do not establish play counts, favorites, or censorship. HLS streaming manifests are outside this workflow.
