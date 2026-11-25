// News-image entry: the front page is drawn by draw.py and stored beside
// this file as entry.png; the program writes that same image out.
// Run outside the grader with MAKEFUN_OUTPUT_DIR set to a scratch dir.

import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const image = readFileSync(new URL('./entry.png', import.meta.url));
writeFileSync(join(outDir, 'entry.png'), image);
