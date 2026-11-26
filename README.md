# Playlist Organizer

Review, group, and reorder music playlists. Preview removals and version swaps before applying them.

## Install

For local agents, copy the entire `skills/playlist-organizer/` folder into the folder listed below. The command-line tools need Python 3.9 or later.

| App | Setup |
| --- | --- |
| Codex | `.agents/skills/` or `~/.agents/skills/`. Run `$playlist-organizer`. |
| Claude Code | `.claude/skills/` or `~/.claude/skills/`. Run `/playlist-organizer`. |
| Claude web and desktop | Enable code execution. Upload the [ZIP](https://github.com/qtaghdi/playlist-organizer-skill/releases/latest/download/playlist-organizer.zip) under **Customize > Skills**. |
| Gemini CLI | `.gemini/skills/` or `~/.gemini/skills/`. The `.agents/skills/` paths also work. |
| Gemini web | Create a Gem with these [instructions](integrations/gemini-gem.md). |
| GitHub Copilot | `.github/skills/` or `~/.copilot/skills/`. |

> Playlist Organizer로 이 플리를 정리해줘. 제목과 곡 순서를 먼저 보여줘.

## Music services

| Service | Input |
| --- | --- |
| [Apple Music](skills/playlist-organizer/references/apple-music.md) | Music XML export |
| [Spotify](skills/playlist-organizer/references/spotify.md) | Account Data playlist JSON and optional Extended Streaming History |
| [YouTube Music](skills/playlist-organizer/references/youtube-music.md) | Takeout playlist CSV and optional track labels |
| [Other services](skills/playlist-organizer/references/portable-inputs.md) | Track list or portable CSV |

Live edits require access to the music app or a supported connection. Keep exports private.

## Command line

```sh
python3 skills/playlist-organizer/scripts/import_export.py spotify Playlist1.json > spotify.csv
python3 skills/playlist-organizer/scripts/import_export.py youtube "My mix.csv" > youtube.csv
python3 skills/playlist-organizer/scripts/audit.py spotify.csv
```

[Skill](skills/playlist-organizer/SKILL.md) · [Planning](skills/playlist-organizer/references/planning.md) · [Track order](skills/playlist-organizer/references/flow.md)
