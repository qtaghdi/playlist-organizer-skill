---
name: playlist-organizer
description: Audit, redesign, and organize music playlists using selectable listening and library signals. Use for stale-song cleanup, personalized grouping, duplicate editions, and clean-to-explicit replacements on supported music services.
---

Help the user decide what belongs in their music playlists and apply the requested changes when supported. Answer in the user's language.

1. Identify the service, source and intended output. Distinguish recommendations, new playlists, edits to selected playlists, and removal from the music library. Reuse the user's choices and offer recommendations for open decisions together. Read [planning.md](references/planning.md) for selectable data and rules.
2. Read the available data. Use [portable inputs](references/portable-inputs.md) for CSV or track lists and [Apple Music](references/apple-music.md) for Music XML, catalog checks, and live edits on macOS. Run `scripts/audit.py` with selected signals and summarize coverage before opening large track-level reports. For other services, inspect the user's export or a supported connection and verify its capabilities before offering live changes.
3. Propose names, counts, representative tracks, cutoff and missing-data handling, and destination. Separate keep, exclude from proposals, remove from specific playlists, replace, and remove from the library. Use stable IDs and preserve source membership and order for replacements. Leave uncertain matches pending.
4. Apply the authorized actions. A design or preview request leaves the source untouched. When irreversible removal lacks clear scope or authorization, show the affected items and ask before applying it. Verify a replacement and any transferred favorite before removing the original. Check existing edits and dependent playlists before library-wide changes. Use native controls or a supported integration, starting with a small verified batch when write behavior is unfamiliar.
5. Re-read affected playlists, library membership, and favorites as applicable. Report verified changes and unresolved items or sync limitations. Keep personal exports, listening data, and change plans out of public repositories.
