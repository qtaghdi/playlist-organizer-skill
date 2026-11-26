# Playlist Organizer

A Codex skill for deciding which songs to keep, how to group them, and which playlist changes to apply. Start with a local CSV, a track list, or an Apple Music XML export.

- Pick the playlists, listening signals, time window, and exceptions. Codex can recommend defaults after inspecting the available data.
- Split tracks by mood, activity, genre, or patterns in your existing playlists. Choose title style and whether tracks can appear in multiple lists. Review the opening, transitions, and runs of alternate versions for sequential listening.
- Plan stale-track cleanup and clean-to-explicit swaps. For a swap, confirm the edition, existing playlist memberships, and favorite state before removing a verified original.

## Install for Codex

Clone the repository, then copy the entire `skills/playlist-organizer` directory to `.agents/skills/` in a project or to `~/.agents/skills/` for your account. Start a new Codex session and invoke `$playlist-organizer`. The local audit requires Python 3.9 or later.

> $playlist-organizer Look at these playlists. Recommend a cutoff from my play history, protect favorites and recent additions, and propose short names for the new playlists. Start with a preview.

> $playlist-organizer 내가 고른 플리의 마지막 재생일과 즐겨찾기를 보고 정리 기준을 추천해줘. 최근 추가한 곡은 두고, 남은 곡은 내가 자주 같이 듣는 곡을 중심으로 나눠줘. 플리 이름은 짧게 하고 먼저 미리보기로 보여줘.

## Inputs and live edits

| Source | How to use it |
| --- | --- |
| CSV or track list from any service | Use the [portable input format](skills/playlist-organizer/references/portable-inputs.md) for grouping and audit. |
| Apple Music on macOS | Choose **File → Library → Export Library**. The skill includes [Apple Music-specific steps](skills/playlist-organizer/references/apple-music.md) for reviewing edits. |
| Other services | Use a supported integration or the service's own controls for live edits when available. CSV and track lists still support a preview and a change plan. |

To inspect a CSV or Apple Music XML file from the repository root:

```sh
python3 skills/playlist-organizer/scripts/audit.py /path/to/export.csv
```

The audit is read-only. Keep exports and reports private. See the [skill](skills/playlist-organizer/SKILL.md), [planning options](skills/playlist-organizer/references/planning.md), and [sequencing and order verification](skills/playlist-organizer/references/flow.md) for the full workflow.
