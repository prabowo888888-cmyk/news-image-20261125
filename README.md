# World News — Wednesday, 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/prabowo888888-cmyk/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/prabowo888888-cmyk/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A make.fun bounty entry: one newspaper-style front page that sums up the
world's news of Wednesday, 25 November 2026, drawn entirely with PIL. The
masthead names the day in large type, then five stories cover five different
beats and regions, each with a coloured tag, a short headline, a two-line
summary and a small drawn motif.

## The five stories

1. **SPACE — Pakistan's first astronaut lifts off for China's Tiangong
   station.** Pakistan Air Force pilot Muhammad Zeeshan Ali rode
   Shenzhou-24 to orbit, the first Pakistani in space and the first
   foreign guest aboard Tiangong.
2. **CONFLICT — Ukraine's drone war reaches the Mediterranean as Putin
   warns of payback.** Kyiv confirmed sea-drone strikes on Russian ships
   off Libya and in the Gulf of Finland; Moscow called them terrorism and
   vowed a response.
3. **MARKETS — AI stocks slide as Trump readies new tariffs on China and
   Europe.** The Nasdaq fell 1.5% and Nvidia about 6% after reports of
   planned tariffs on China, the EU and 14 more economies; Micron dropped
   11%.
4. **TECH — US jury convicts Huawei of stealing trade secrets and bank
   fraud.** A Brooklyn jury found the Chinese telecom giant guilty on 10
   of 12 counts but cleared it of racketeering; Huawei says it will
   appeal.
5. **MIDDLE EAST — Iraq orders federal forces to seize Kurdish
   oilfields.** Baghdad told its troops to take over oilfields and
   crossings in Kurdish-run areas; Kurdish leaders rejected the order
   outright.

Sources checked against the morning wires of 25 November 2026: Reuters,
AP, the US Department of Justice and Al Jazeera.

## How it works

`gen_image.py` draws the 1024x1024 front page and saves it as `entry.png`
in this repository. `main.py` copies that bundled image to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), byte for byte, so the
two grader runs produce identical files.

## Run it

```sh
python3 gen_image.py          # redraw entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
