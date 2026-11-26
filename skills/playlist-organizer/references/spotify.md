# Spotify

## Read the user's source

Use a user-supplied track list or the playlist JSON from the user's Spotify **Download your data** account export. The local converter understands an Account Data file with a `playlists` array and nested song records. Use the portable CSV format for another shape. The converter reads selected names and preserves source ordering and repeated occurrences. It reports unavailable items, non-song entries, and lists with no usable rows. Review these omissions before changing a live playlist. The generated playlist IDs are local to the input file. Resolve the actual Spotify playlist URL and ownership separately.

```sh
python3 scripts/import_export.py spotify Playlist1.json --playlist "Mix" > mix.csv
python3 scripts/audit.py mix.csv
```

If the user wants listening analysis and supplies Extended Streaming History, add each distinct, non-overlapping JSON file using `--history`. The converter joins by exact Spotify track URI and emits only the latest qualifying play timestamp and count for selected songs. It defaults to a 30-second minimum and accepts `--min-ms` for a different threshold. Treat missing matches as unknown. A history export can contain sensitive device and account details. Keep the source local and use the minimized CSV when sharing is authorized.

```sh
python3 scripts/import_export.py spotify Playlist1.json --playlist "Mix" \
  --history Streaming_History_Audio_0.json --min-ms 30000 > mix.csv
```

The playlist export does not by itself establish last-played dates, Liked Songs membership, or clean-to-explicit equivalence. Use an exact-ID favorite list if the user supplies one. Spotify's developer policy restricts ingesting Spotify Web API content into AI. This skill uses the personal export workflow and includes no Spotify Web API client.

## Apply authorized changes

Use Spotify's app controls for supported live edits when available. Verify the editable playlist and exact edition in the user's market. Confirm the replacement's membership and saved state before removing the original. Treat **Liked Songs** and a normal playlist as separate locations. Avoid interpreting an unmarked edition as a verified clean counterpart. If the app exposes a different recording with an identical title, compare the artist, credits, album, and duration.

For order changes, use the playlist's editable order when supported. Preserve repeated occurrences and check the live count and positions. Return a verified draft or a change list when the host cannot edit the user's Spotify app.

- [Spotify account data export fields](https://support.spotify.com/us/article/understanding-your-data/)
- [Spotify playlist controls](https://support.spotify.com/us/article/create-playlists/)
- [Spotify Developer Policy](https://developer.spotify.com/policy)
