import type { APIRoute } from 'astro';
import { sampleCsv } from '../sample-playlist';

export const GET: APIRoute = () => new Response(sampleCsv, {
  headers: { 'Content-Type': 'text/csv; charset=utf-8' },
});
