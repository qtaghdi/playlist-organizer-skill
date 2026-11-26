# Playlist Organizer

An Agent Skill for deciding which songs to keep, how to group and sequence them, and which changes to apply. Pick your AI host and music service independently.

- Choose listening signals, a cutoff, and exceptions based on available data.
- Build playlists around mood, activity, genre, or the user's listening patterns. Review openings and transitions before applying an exact order.
- Preview stale-track removals and edition swaps. Verify the destination version and any transferred favorites before removing the verified original.

## Install in your AI host

Copy the whole `skills/playlist-organizer` directory to a path below, or use the upload option. The bundled local tools require Python 3.9 or later.

| AI host | Install and use |
| --- | --- |
| Codex | Copy into `.agents/skills/` or `~/.agents/skills/`. Invoke `$playlist-organizer`. [Codex installation paths](https://developers.openai.com/api/reference/cli) |
| Claude Code | Copy into `.claude/skills/` or `~/.claude/skills/`. Invoke `/playlist-organizer`. [Claude Code skills](https://code.claude.com/docs/en/skills) |
| Claude web and desktop | Download `playlist-organizer.zip` from [Releases](https://github.com/qtaghdi/playlist-organizer-skill/releases/latest) and upload it in **Customize → Skills** with code execution enabled. [Claude skills](https://support.claude.com/en/articles/12512180-use-skills-in-claude) |
| Gemini CLI | Copy into `.gemini/skills/` or `~/.gemini/skills/`. The `.agents/skills/` paths also work. Ask Gemini CLI to use Playlist Organizer and confirm activation when prompted. [Gemini CLI skills](https://geminicli.com/docs/cli/skills/) |
| Gemini web | Create a Gem and paste the [Gem instructions](integrations/gemini-gem.md). Upload only the track data you want to analyze. [Gem setup](https://support.google.com/gemini/answer/15235603) |
| GitHub Copilot | Copy into `.github/skills/` for a project or `~/.copilot/skills/` for your account. [Copilot Agent Skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) |

> Use Playlist Organizer with this CSV. Compare a six-month cutoff with what my history can actually support, then draft short playlists with a coherent listening order.

> Playlist Organizer로 내가 고른 플리를 정리해줘. 재생 기록이 있는 곡을 기준으로 정리 기간을 추천하고, 새 플리의 제목과 순서를 먼저 보여줘.

## Choose a music service

| Service | Analysis inputs | Applying the plan |
| --- | --- | --- |
| [Apple Music](skills/playlist-organizer/references/apple-music.md) | Music on Mac XML or a portable list | Mac Music or another supported, authorized connection |
| [Spotify](skills/playlist-organizer/references/spotify.md) | Personal playlist export JSON, optional Extended Streaming History, or a portable list | Spotify's editing controls when available |
| [YouTube Music](skills/playlist-organizer/references/youtube-music.md) | Takeout playlist CSV, optional track labels, or a portable list | YouTube Music controls or authorized supported playlist operations |
| [Other services](skills/playlist-organizer/references/portable-inputs.md) | CSV or track list | An available, authorized integration, or an ordered change plan |

Installing the skill gives the agent the workflow. Live edits require tools and permissions for the selected service. Keep personal exports and reports private.

## Run the local tools

```sh
python3 skills/playlist-organizer/scripts/import_export.py spotify Playlist1.json > playlist.csv
python3 skills/playlist-organizer/scripts/import_export.py youtube "My mix.csv" --metadata track-labels.csv > playlist.csv
python3 skills/playlist-organizer/scripts/audit.py playlist.csv
```

See the [skill](skills/playlist-organizer/SKILL.md), [planning options](skills/playlist-organizer/references/planning.md), and [sequencing and order verification](skills/playlist-organizer/references/flow.md) for the full workflow.
