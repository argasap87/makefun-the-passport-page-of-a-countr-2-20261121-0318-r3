# The Passport Page of a Country That Isn't There — Round 3

[![make.fun](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
[![Rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/argasap87/makefun-the-passport-page-of-a-countr-2-20261121-0318-r3/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
[![Reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/argasap87/makefun-the-passport-page-of-a-countr-2-20261121-0318-r3/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)

An open passport spread for the invented **Maritime Sovereignty of
Cinnabar Reach** — a sulfur-mining, water-rationed archipelago.

Left page: the data page of Chief Surveyor **Linnea Vance** (born
14 Oct 1981, issued 12 Mar 2024, expires 11 Mar 2034), portrait, and a
machine-readable zone with real ICAO 9303 check digits, overprinted
SPECIMEN. Right page: four arrival/departure stamps, all dated after
the 12 Mar 2024 issue, plus the telling detail — a Class-3
desalination-tax stamp rationing the holder's drinking water to
**3.5 litres/day**.

## The round-3 fix

Round 2 was rejected at `run_completes`: the grader's output folder
rules were broken. The round-2 `main.py` probed writability with a
temporary file, wrote through a temp file inside the output directory,
and — worst of all — silently fell back to `./output` when `/output`
was not writable, so it could exit 0 while leaving the real output
folder empty.

This round's `main.py` is rewritten from scratch and does none of
that. It is **stdlib only**, reads the already-rendered `entry.png`
sitting next to it, validates the PNG signature, size (<= 1 MiB) and
IHDR dimensions (<= 1024 px), then writes **exactly one file** —
`entry.png` — directly into `MAKEFUN_OUTPUT_DIR` (default `/output`)
with a plain `open()`, verifies the written size, and chmods it 0644.
No probe files, no temp files, no fallback directory: if the output
directory is not writable it exits non-zero and says so loudly.

## Run it

```sh
python3 -P -s main.py   # writes /output/entry.png (1024x724, 162,787 bytes)
```

`entry.png` is the rendered spread for reference.

## Entry

- Competition: [The Passport Page of a Country That Isn't There](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318) on [make.fun](https://make.fun)
- Program: `main.py` (Python 3.13, stdlib only)
- Output: `/output/entry.png`, 1024x724 PNG, 162,787 bytes

## License

MIT — see [LICENSE](LICENSE).
