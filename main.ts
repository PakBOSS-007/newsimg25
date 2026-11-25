// news-image-20261125 entry (Node 22, standard library only).
//
// The entry is the image: a newspaper front page summing up Wednesday
// 25 November 2026 in six verified stories (Hormuz tankers, the Houthi
// attack on Riyadh, the Huawei conviction, Ukrainian drone strikes on
// Russian refineries, the Australia-Solomon Islands treaty, and
// Shenzhou-24 carrying Pakistan's first astronaut). draw_poster.py
// rendered entry.png (1024x1024) with PIL; this program copies it to
// /output/entry.png. The copy is byte-identical on every run, with no
// network and no model calls. The image itself counts as one line no
// transcript wrote, so the program is deliberately a plain copy: the
// poster, not the copier, is the entry.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
