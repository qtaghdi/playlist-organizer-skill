# Apple Music Playlists

A Codex skill that audits your Apple Music playlists, suggests cleanup rules based on your listening, and helps you organize the tracks you want to keep.

- Pick the playlists, time window, exceptions, and listening signals. Codex can recommend defaults after inspecting the available data.
- Split tracks by mood, activity, genre, or patterns in your existing playlists. Choose title style and whether tracks can appear in multiple lists.
- Plan stale-track cleanup and clean-to-explicit swaps. The skill checks the edition, existing playlist memberships, and favorite state before removing a verified original.
- Use an Apple Music XML export for an offline preview. The included Python tool is read-only. Live edits use Music or an available supported integration.

## Install for Codex

Clone the repository, then copy the entire `skills/apple-music-playlists` directory to `.agents/skills/` in a project or to `~/.agents/skills/` for your account. Start a new Codex session and invoke `$apple-music-playlists`. The offline audit requires Python 3.9 or later.

> $apple-music-playlists Look at my selected playlists. Recommend a cutoff from my play history, protect favorites and recent additions, and propose short names for the new playlists. Start with a preview.

> $apple-music-playlists Help me replace clean editions with verified explicit counterparts in my selected playlists. Carry over favorites and flag songs whose alternate edition is uncertain.

## Start with an export

In Music on Mac, use **File → Library → Export Library** and save the XML locally. Give Codex the export path and the playlists it should consider. The export's track and playlist coverage depends on the Apple Music client and sync state. Existing playlists and favorites can also be inspected directly when Music is available.

To inspect the file yourself from the repository root:

```sh
python3 skills/apple-music-playlists/scripts/audit.py /path/to/library.xml
```

See the [skill](skills/apple-music-playlists/SKILL.md) for the workflow and [planning options](skills/apple-music-playlists/references/planning.md) for the inputs you can choose. Keep your XML exports and listening reports private.

## 한국어로 사용하기

> $apple-music-playlists 내가 고른 플리의 마지막 재생일과 즐겨찾기를 보고 정리 기준을 추천해줘. 최근 추가한 곡은 두고, 남은 곡은 내가 자주 같이 듣는 곡을 중심으로 나눠줘. 플리 이름은 짧게 하고 먼저 미리보기로 보여줘.

> $apple-music-playlists 검열판을 미검열판으로 바꿀 후보를 찾아줘. 원래 플리와 즐겨찾기를 이어받을 수 있는지 확인하고, 같은 녹음인지 확실하지 않으면 보류해줘.
