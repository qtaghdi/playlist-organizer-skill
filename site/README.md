# Landing page

Use Node.js 24.

```sh
npm ci
npm run dev
npm run build
```

Open the `/playlist-organizer-skill/` path on the local server. GitHub Actions publishes the static build from `main`.

## Listening example

`src/listening-demo.json` records two Codex runs using Playlist Organizer with the same four fictional tracks. The first run preserved the input order. The second also read the saved listening note and moved `Over the Water` from third to second. The sample CSV is generated from the same data.

## Artwork

The Playlist Organizer mark, favicon, record illustration, and fictional track list were created for this project. The artwork is covered by the repository's MIT license. The site uses system fonts and identifies compatible services by name.
