# Hero card prompt — Game Boy / Game Boy Color (v2-gb)

The GBA prompt (`PROMPT.md`, v2) with the changes a Game Boy cover needs. Every
layout rule is unchanged: the browser prints the title and file size in the
same place whichever console is active, so a GB card has to leave the same
quiet left half as a GBA one.

## What differs from the GBA prompt, and why

**1. The spine is different.** GB and GBC covers carry a vertical "GAME BOY"
or "GAME BOY COLOR" wordmark down the LEFT edge on a grey/silver or white
strip, plus a Nintendo "Official Seal" badge. Both must go, the same as the
GBA spine did.

**2. Some covers are almost all logo.** Link's Awakening's box is a gold field
with the Zelda crest and a sword; Tetris is a wordmark over falling blocks.
Removing the text leaves nothing to extend. For those, the per-game note in
`prompts_gb.json` names the scene to paint instead, drawn from the game
itself, in the style of the game's own official artwork of the period. That
is re-staging taken one step further, and it is the only honest option.

**3. The palette rule is loosened for monochrome-era games.** A Game Boy game
has no in-game colour to match; its official art does. Match the OFFICIAL
ILLUSTRATION'S palette, never the green-grey screen, and never render the art
as pixel art or as a DMG screenshot.

## The prompt

```
Extend and clean this {CONSOLE} box art into a widescreen wallpaper.

SOURCE
This is the front cover of {GAME}. Preserve its characters, colour palette
and illustration style — the same artist's hand. Match the GAME'S OWN TONE: a
bright comedic game stays bright and comedic, a mysterious one mysterious, a
cute one cute. Do not default to dark epic fantasy. Do not render it as pixel
art or as a Game Boy screenshot: this is the painted cover art, extended.

{GAME_NOTE}

WHEN FIDELITY AND LAYOUT CONFLICT, LAYOUT WINS
Many Game Boy covers put the subject dead centre, filling the frame. Such a
composition CANNOT be extended outward and still leave a quiet left half —
the subject is already there. In that case do not force it: RE-STAGE the
scene. Move the subject into the right half and build new environment around
it. Re-staging is expected and correct for centre-dominant covers.

What must survive re-staging: the characters themselves (recognisable and
on-model), the palette, the art style, and the mood. What may change: where
things sit, the camera angle, and how much environment surrounds them.

OUTPUT
16:9 landscape, at least 960x544 (larger is fine — it is downscaled later).
No borders, no frame, no letterbox bars, edge to edge.

It will be displayed on a 480x272 screen, so favour bold readable shapes over
fine detail: thin lines, small text and fine texture all disappear at that size.

REMOVE COMPLETELY
- the game's title, logo and all wordmarks
- the vertical "GAME BOY" / "GAME BOY COLOR" spine down the left edge, and
  its grey, silver or white strip
- the Nintendo "Official Seal", ESRB / PEGI rating badges
- publisher and developer logos (Nintendo, Game Freak, Capcom, etc.)
- "Gotta catch 'em all!", "Only for Game Boy Color", "Includes new secret
  dungeon!", taglines, starbursts, stickers, banners
- any text of any kind, in any language

EXTEND
The cover is roughly square; the output is widescreen. Paint new artwork
outward in the same style, continuing the scene naturally — environment, sky,
atmosphere. Do not mirror or repeat existing elements. Do not invent
characters or objects the original (or the game note above) does not imply.

COMPOSITION
- The LEFT 55% must stay visually QUIET: open sky, mist, water, gradient,
  shadow, blurred distance. Low contrast, low detail, darker than the right.
  White text is printed over this region and must remain readable. Nothing
  with hard edges or bright highlights belongs there.
- The main subject sits in the RIGHT HALF.
- KEEP THE FRAMING CONSISTENT ACROSS ALL IMAGES. The subject should occupy a
  similar share of the frame every time, in a similar position.
- Exposure slightly dark overall, lit for a dark interface. Rich colour is
  good; blown highlights in the left half are not.

CRITICAL — NO BANDS
Do NOT paint a dark bar, band, gradient strip or panel across the bottom of
the image. Do NOT letterbox. The artwork must run cleanly to all four edges
with no horizontal seam anywhere. Any darkening the interface needs is added
later in software.

STYLE
Cinematic, atmospheric, painterly — a game's title-screen background, not a
photograph of a box.

DO NOT
No text. No borders, vignette frames or bars. No collage or panels. No UI
mockups. No logos. No watermarks. No pixel art.
```

`{CONSOLE}` is "Game Boy" or "Game Boy Color"; `{GAME_NOTE}` is the per-game
line from `prompts_gb.json` (empty when the cover extends on its own).

## Filenames

Same rule as GBA: the card is matched to the ROM by exact filename stem, and
it goes in the same `hero/` folder. `Pokemon - Crystal Version (USA, Europe)
(Rev 1).gbc` wants `hero/Pokemon - Crystal Version (USA, Europe) (Rev 1).png`.
The names here are No-Intro's; a dump from your own cartridge with a different
name is what HeroForge's re-match is for.
