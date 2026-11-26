# Listening notes

A playlist name and a short note are enough. A track or pair of tracks makes a note easier to apply.

```text
Evening | Harbor Lights → Paper Moon | Keep this transition
Walk | Overdrive | Too loud here
여운 | 잔잔한 곡 A 다음에 잔잔한 곡 B | 이 순서 좋아
```

When the user asks to save feedback, use their chosen notes file or `.playlist-organizer/feedback.md` in the private workspace they use for playlist work. Record the location so they can use the same file from another AI host. Keep the user's wording. Add short artist names or stable IDs only when needed to distinguish versions or playlists. Keep notes out of shared repositories and release bundles. Attaching the notes file works in cloud hosts that cannot access the original workspace.

A user can ask in chat. The script is optional when they prefer a terminal.

```sh
python3 scripts/feedback.py "여운 | 잔잔한 곡 A 다음에 잔잔한 곡 B | 이 순서 좋아"
python3 scripts/feedback.py "Walk | Overdrive | Too loud here" --file /path/to/private-feedback.md
```

## Apply notes on the next pass

1. Read feedback supplied in the conversation or saved for the current playlist scope before suggesting groups or order. Use the user's listening judgment ahead of inferred genre or energy.
2. Resolve notes against current playlist and track identities. A liked transition preserves that direction. A track that feels out of place is a candidate to move or reorder within the requested scope. Treat a disliked transition separately from a disliked song. A note on one recording does not automatically apply to other versions or playlists.
3. Follow the user's latest clear correction. Keep unresolved names and conflicting notes visible when they would change the result. Saving a note alone does not authorize an edit or deletion.
4. Check the plan against each relevant note. After applying an ordered change, verify any requested adjacency in the observed playlist and report notes that remain unresolved.
