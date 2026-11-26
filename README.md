# Playlist Organizer

Review, group, and reorder music playlists. Preview removals and version swaps before applying them.

## Install

[Find setup steps for your AI app](https://qtaghdi.github.io/playlist-organizer-skill/#install).

In Codex, paste this request into a chat:

```text
Use $skill-installer to install Playlist Organizer from https://github.com/qtaghdi/playlist-organizer-skill/tree/main/skills/playlist-organizer
```

You can also install from a terminal:

```sh
npx --yes skills add qtaghdi/playlist-organizer-skill --skill playlist-organizer -a codex -g -y
```

For manual installation, copy the entire `skills/playlist-organizer/` folder into the folder listed below. The command-line tools need Python 3.9 or later.

| App | Setup |
| --- | --- |
| Codex | `.agents/skills/` or `~/.agents/skills/`. Run `$playlist-organizer`. |
| Claude Code | `.claude/skills/` or `~/.claude/skills/`. Run `/playlist-organizer`. |
| Claude web and desktop | Upload the [ZIP](https://github.com/qtaghdi/playlist-organizer-skill/releases/latest/download/playlist-organizer.zip) from **Plugins > Add > Upload plugin**. On the older interface, use **Customize > Skills**. |
| Gemini CLI | `.gemini/skills/` or `~/.gemini/skills/`. The `.agents/skills/` paths also work. |
| Gemini web | Ask Gemini to create a skill from these [instructions](integrations/gemini-gem.md), then select `@playlist-organizer` in a new chat. If your account still has Gems, paste the instructions into a new Gem. |
| GitHub Copilot | `.github/skills/` or `~/.copilot/skills/`. |
| Cursor | `.cursor/skills/` or `~/.cursor/skills/`. [Setup](https://cursor.com/docs/skills) |
| OpenCode | `.opencode/skills/` or `~/.config/opencode/skills/`. Use `@playlist-organizer`. [Setup](https://opencode.ai/docs/skills/) |

> Playlist Organizer로 이 플리를 정리해줘. 제목과 곡 순서를 먼저 보여줘.

## Listening notes

Leave one line in chat or a private notes file. Use the same file next time.

```text
새벽 | 곡 A 다음에 곡 B | 이 순서 좋아
```

[Save and apply notes](skills/playlist-organizer/references/feedback.md)

## Music services

| Service | Input |
| --- | --- |
| [Apple Music](skills/playlist-organizer/references/apple-music.md) | Music XML export |
| [Spotify](skills/playlist-organizer/references/spotify.md) | Account Data playlist JSON and optional Extended Streaming History |
| [YouTube Music](skills/playlist-organizer/references/youtube-music.md) | Takeout playlist CSV and optional track labels |
| [M3U and M3U8](skills/playlist-organizer/references/m3u.md) | Local playlist file. Read it or save a new order. |
| [Other services](skills/playlist-organizer/references/portable-inputs.md) | Track list or portable CSV |

[Last.fm and ListenBrainz](skills/playlist-organizer/references/history.md) can add play history to a CSV.

Live edits require access to the music app or a supported connection. Keep exports private.

## Command line

```sh
python3 skills/playlist-organizer/scripts/import_export.py spotify Playlist1.json > spotify.csv
python3 skills/playlist-organizer/scripts/import_export.py youtube "My mix.csv" > youtube.csv
python3 skills/playlist-organizer/scripts/audit.py spotify.csv
```

[Skill](skills/playlist-organizer/SKILL.md) · [Planning](skills/playlist-organizer/references/planning.md) · [Track order](skills/playlist-organizer/references/flow.md)
