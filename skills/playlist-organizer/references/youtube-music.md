# YouTube Music

## Read the user's source

Use a track list with title and artist, an authorized source, or a local playlist CSV from the user's YouTube and YouTube Music Google Takeout archive. Select only needed files. The converter supports a `Video ID` column, including exports with playlist metadata before the track rows. It preserves the supplied row order and duplicates. The CSV may give only IDs and time added. Time added to a playlist cannot establish time listened.

```sh
python3 scripts/import_export.py youtube "My mix.csv" --playlist "My mix" > mix.csv
```

Supply an optional user-owned metadata CSV with `track_id,title,artist` and optional `album` to label those IDs before grouping. Missing labels are explicit placeholders. An ID-only file supports membership and order checks. It cannot tell you which songs have similar sounds. Keep playlist and history exports private.

```sh
python3 scripts/import_export.py youtube "My mix.csv" --metadata track-labels.csv > mix.csv
python3 scripts/audit.py mix.csv
```

## Apply authorized changes

Use the YouTube Music app for music-specific edits and verification. Match the exact recording and check whether the result is the official song, a video of that song, a live version, a remix, or a cover. A shared YouTube playlist can appear in both products and still display a different set of playable items in YouTube Music. Verify important changes in YouTube Music itself. Treat Liked Music separately from ordinary playlist membership and keep likes tied to the exact recording.

The YouTube Data API documents standard playlist operations. If an authorized integration exposes those operations and its use complies with the YouTube API policies, distinguish the playlist item ID (occurrence) from the video ID (recording or video). Fetch all pages, verify edit permissions and manual ordering, and re-read the changed occurrences. Use YouTube Music controls for anything the connection does not support or verify.

Gemini Apps can create a playlist or radio when YouTube Music is connected and the feature is available. Verify the resulting tracks and save state. Use a plan or the YouTube Music app for exact edits to existing playlists if the connection cannot perform them.

- [Download data with Google Takeout](https://support.google.com/accounts/answer/3024190)
- [Make or edit a YouTube Music playlist](https://support.google.com/youtubemusic/answer/7205933?co=GENIE.Platform%3DDesktop)
- [YouTube Data API playlist items](https://developers.google.com/youtube/data/reference/rest/v3/playlistItems)
- [YouTube API policies](https://developers.google.com/youtube/terms/developer-policies)
- [YouTube Music in Gemini Apps](https://support.google.com/gemini/answer/15237118)
