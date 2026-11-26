# Planning playlist changes

## Choose the inputs

Use only the information needed for the requested actions. Users can opt into or out of each signal. Explain the trade-off when omitting a signal prevents a requested decision.

| Input | What it supports |
| --- | --- |
| Track identity, title, artist and selected playlist membership | Baseline for reading a playlist, placing tracks and identifying the exact item to change |
| Album, track/disc position and duration | Compare recordings, remasters, edits and versions |
| Last played and date added | Recency cutoff, with an option to protect recent additions |
| Play counts, skip counts and skip dates | Rank familiarity or friction, interpreted in context of track age, device sync and sparse coverage |
| Favorites, ratings and dislikes when available | Protect or rank liked tracks, and transfer a favorite when replacing its song |
| Existing playlist overlap and order | Learn which tracks the user already listens to together and preserve deliberate sequences |
| Genres, artist patterns, mood, activity, user anchors, lyrics language, tempo or energy | Group or order tracks when those signals are known. Optional labels supplied by the user are valid. Do not infer language from storefront or tempo from genre labels |
| Music catalog and store region | Verify available editions when the user allows a catalog lookup. Send the minimum search terms required for the specific match |
| Additional history or curated track lists supplied by the user | Fill coverage gaps. Match using stable identifiers first and leave ambiguous title/artist matches unresolved |

For a large library, summarize date coverage, playlist sizes, favorite coverage when known, and dominant genres or playlist overlap before recommending defaults. An export may omit data for songs found only in playlists or activity from other devices. Missing fields represent unknowns.

## Choose the rules and deliverables

- **Scope and destination.** Select existing playlists, their folder, or the library. Choose new playlists, edits to source playlists, or a preview. Keep stale-song playlist removal distinct from library removal. Use the chosen folder and avoid reusing a personal naming scheme from another user.
- **Recency.** Suggest a window from the observed distribution and the stated goal, such as three, six or twelve calendar months. Show how many items each viable threshold would affect. State the cutoff date, timezone, and inclusive boundary. Preserve unknown dates by default. A user can explicitly choose to review or exclude tracks with unknown history and old add dates. Keep recently added and playlist-only tracks in review when their listening coverage is unclear. Let the user choose protections for favorites, pinned playlists, seasonal tracks or exceptions by artist.
- **Versions and duplicates.** Let the user keep current editions, prefer explicit, prefer clean, or review flagged tracks. Treat the presence of a verified alternate as distinct from permission to replace it. Suggest exact duplicate cleanup separately from edition changes. Keep alternate recordings such as live, acoustic, remix, edited, and re-recorded versions separate unless the user requests otherwise.
- **Grouping.** Offer ways to split the remaining tracks by activity, mood, genre, language, energy, or familiar combinations found in the selected playlists. Ask for or suggest the number and size, title style and language, overlap policy, anchor tracks, and ordering. Use verified features when available. Use existing co-membership as evidence of taste and play counts or favorites as evidence of familiarity. For a new playlist, give sample tracks before committing to the split. Keep seasonal or unusual use cases intact when the evidence supports a separate list.
- **Changes and privacy.** Offer a summary, proposed track lists, or a verified edit. The user can choose which optional signals to use and whether to look up catalog data. Export locally and keep source data and outputs private unless the user asks to share them.

## Check the plan

Use stable playlist IDs, track IDs and, where applicable, the position or number of occurrences for changes. Snapshot numeric track IDs are valid for joins within that export. Before live changes, re-resolve identities from persistent IDs or a verified catalog ID.

For exclusive grouping, every retained track should appear once unless it is explicitly deferred. For overlapping grouping, report both unique tracks and total playlist entries. Resolve unintended empty lists, name clashes, favorite transfers, unresolved IDs, and duplicate actions before applying. Preserve relative order and deliberate duplicate entries in existing playlists where the client supports exact edits. Explain any unsupported edit before changing that playlist.
