import type { APIRoute } from 'astro';
import demo from '../listening-demo.json';

const tracks = new Map(Object.entries(demo.tracks));
const csvField = (value: string) => `"${value.replaceAll('"', '""')}"`;

export const GET: APIRoute = () => {
  const header = 'playlist_id,playlist,track_id,title,artist';
  const rows = demo.order.before.map((id) => {
    const track = tracks.get(id)!;
    return [demo.playlistId, demo.name, id, track.title, track.artist].map(csvField).join(',');
  });

  return new Response([header, ...rows, ''].join('\r\n'), {
    headers: { 'Content-Type': 'text/csv; charset=utf-8' },
  });
};
