# Apple Music sources and changes

## Read

On a Mac with Music, export locally with **File → Library → Export Library**. An authorized macOS session can also use Music's AppleScript export command. Use an unused absolute destination in a private working directory.

```applescript
tell application "Music" to export source 1 to POSIX file "/absolute/private/path/library.xml"
```

A single-playlist XML export can be useful for analysis, but it cannot establish full library membership or other playlists affected by a replacement. For XML analysis, see `python3 scripts/audit.py --help`. Run the examples from the skill directory. Use Python 3.9+.

```sh
python3 scripts/audit.py /path/to/library.xml
python3 scripts/audit.py /path/to/library.xml --playlist PLAYLIST_ID --signals recency,genre,favorites,versions --cutoff YYYY-MM-DD --timezone UTC --protect-favorites --tracks
```

The default inventory lists playlists and their IDs. An explicit `--library` selects downloaded and cloud library tracks present in the export, excluding records marked playlist-only. `--playlist` selects playlist members, including playlist-only tracks. Omit `--tracks` for counts. When names repeat, use the ID and parent ID. XML absence of a subscription playlist or a system playlist does not prove it is absent from the app. Confirm live playlist type, ownership, and editability before writes.

Read Music's built-in scripting dictionary with Script Editor before relying on AppleScript to resolve tracks or playlists, and use supported Music controls for operations the dictionary cannot verify. A preview works with an exported file on other operating systems. A live write requires a supported authenticated integration or access to the Music app and the relevant controls.

## Verify editions

1. Read clean and explicit flags from the same export or an authorized Apple catalog response. An absent rating does not establish censorship or a verified explicit release.
2. Search the user's storefront by song and artist, then compare release, track/disc position, duration and version labels. Prefer the same release family and recording. A title match alone is insufficient. Use an available explicit catalog ID and record the evidence. If more than one plausible recording remains, hold the item for review.
3. Before changes, record the old track's memberships and favorite state. Add or reuse the verified counterpart. Check the title, artist, version, membership, and favorite on the new track. If the original was favorited, favorite the replacement and confirm it in Music. Preserve any existing favorite on the replacement.
4. Verify each updated playlist before removing the old entry in the approved scope. Preserve playlist positions if supported. Check whether library-wide removal will affect other playlists and synced devices. If the original is still referenced outside the approved scope, retain it there and report the dependency.

A catalog button changing state may reflect a catalog match to a song already in the library. Confirm that the target edition exists as its own library record with the right rating before deleting the source. If a web addition has not appeared in Music on Mac, check that the same library is open, use **File → Library → Update Cloud Library** when available, and re-read after sync. If a temporary favorite was used to make the exact replacement available and the final plan does not call for that favorite, clear the temporary mark and verify that the new track remains in the library. After removing a clean favorite, recheck the explicit favorite on the matching catalog item after sync. If the cloud drops it, restore the favorite on the exact replacement and verify again.

Apple Music may not transfer history or counts between catalog versions. Use those signals for grouping without fabricating playback history for a replacement.

## Apply and verify

Use native Music controls or supported authenticated tooling. For folder organization, create named standard playlists and add them to the selected folder. Test position changes on a small batch. Music may append a copied track even when an insertion position is supplied. When resequencing in place, confirm the current sequence and the staged target entries before removing superseded occurrences, and re-read the exact order afterward. Preserve the playlist identity when feasible. Smart playlists follow their rules. Treat shared, collaborative and subscription playlists as read-only until actual editability and authorized scope are established.

For sourced track removal, use the playlist's removal action. Library removal is a separate action. Check the actual dialog and settings before accepting a removal. An XML export is an inventory and a partial recovery aid. It cannot recover local media, sync history, or every preference.

Keep a local list of completed actions and re-read state before retrying a partial operation. Compare counts and persistent IDs after edits, including the destination folder, selected playlist memberships, favorites, and the presence or absence of the original track. Confirm cloud sync separately when observable.

- [Export a library or playlist](https://support.apple.com/guide/music/save-a-copy-of-a-playlist-mus27cd5060f/mac)
- [Apple Music content ratings and alternate versions](https://developer.apple.com/documentation/applemusicapi/managing-content-ratings-alternate-versions-and-equivalencies)
- [Create and edit playlists](https://support.apple.com/guide/music/create-edit-and-delete-playlists-musd5d051981/mac)
- [Organize playlists in folders](https://support.apple.com/guide/music/organize-playlists-in-folders-musb6032bb56/mac)
- [Delete songs and other items](https://support.apple.com/guide/music/delete-items-mus51db94bb1/mac)
