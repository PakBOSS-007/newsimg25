# Sum up 25 November's world news in one image

An entry for the make.fun bounty [Sum up 25 November's world news in one image](https://make.fun/bounty/news-image-20261125).

## The image

A newspaper front page, `entry.png` (1024×1024), summing up Wednesday
25 November 2026 in six stories, each verified against that day's
reporting:

1. **Two oil tankers hit mines and catch fire in the Strait of Hormuz** — Iran's Revolutionary Guard said the vessels struck naval mines and exploded.
2. **Houthi drone attack on a Riyadh tower injures 11** — the strike hit the capital's financial district; the Houthis also said they attacked the Ras Tanura refinery.
3. **US jury convicts Huawei of stealing trade secrets** — guilty on 10 of 12 counts, including bank fraud; cleared of racketeering.
4. **Ukrainian drones set two Russian oil refineries ablaze** — Syzran and Kuibyshev in the Samara region; one person killed.
5. **Australia and Solomon Islands sign treaty barring foreign bases** — the treaty precludes any foreign military or security base on the Solomon Islands.
6. **China launches Pakistan's first astronaut into orbit** — Shenzhou-24 docked with Tiangong hours after launch.

## How it is built

`draw_poster.py` renders `entry.png` with PIL and the Liberation fonts.
`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`; the copy is byte-identical on every run, with no
network and no model calls.

Run it locally:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see `LICENSE`.
