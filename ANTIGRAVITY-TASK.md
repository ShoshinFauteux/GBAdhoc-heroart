# Task for the Antigravity agent: 10 GB/GBC hero cards

Open this folder (`GBAdhoc-heroart-gb`) in Antigravity and give its agent this
file. Everything it needs is here.

For each of the 10 games below:

1. Take the cover `boxart-gb/<stem>.png` as the reference image.
2. Use the prompt in `prompts_gb_full/<stem>.txt` exactly as written. It is
   PROMPT-GB.md with the game's note filled in; do not shorten it.
3. Generate ONE 16:9 image (1376x768 or larger) with your image model.
4. Save it as `masters/<stem>.png`: the EXACT stem, same spaces, commas and
   parentheses, `.png`. Cards are matched to ROMs by filename and nothing else.
5. Check it before moving on: no text or logos anywhere, no "GAME BOY" spine
   down the left edge, the left ~55% quiet and dark enough for white text, the
   subject in the right half, and NO dark band or seam along the bottom. If it
   fails, regenerate it.

Stems:

```
Pokemon - Red Version (USA, Europe) (SGB Enhanced)
Pokemon - Blue Version (USA, Europe) (SGB Enhanced)
Tetris (World) (Rev 1)
Legend of Zelda, The - Link's Awakening (USA, Europe)
Super Mario Land 2 - 6 Golden Coins (USA, Europe)
Pokemon - Gold Version (USA, Europe) (SGB Enhanced) (GB Compatible)
Pokemon - Silver Version (USA, Europe) (SGB Enhanced) (GB Compatible)
Pokemon - Crystal Version (USA, Europe) (Rev 1)
Legend of Zelda, The - Link's Awakening DX (USA, Europe) (Rev 2) (SGB Enhanced) (GB Compatible)
Legend of Zelda, The - Oracle of Seasons (USA, Australia)
```

When all 10 are in `masters/`, run:

```
python build.py
```

That debands, resizes to 480x272 and writes the PSP-ready files to
`build/pack/hero/`. Copy that folder's contents to
`PSP/GAME/GBADHOC/hero/` on the memory stick.

Do not edit any other file in this folder.
