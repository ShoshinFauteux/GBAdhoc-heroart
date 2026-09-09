# Hero card prompt — v2

The first pass was very good. Three things to change, one of which was my
error in v1.

## What changed and why

**1. The bottom dark band — MY MISTAKE, remove it entirely.**
v1 said "the bottom 45 pixels must be calm and dark". That got painted as a
literal dark rectangle with a hard horizontal edge, and it appears in all
twelve images. It reads as a letterbox bar or a UI panel rather than as
artwork. The emulator can draw that scrim itself in code, as a true gradient,
so the art must NOT contain one.

**2. KEEP the framing consistent.** I initially called the repetition a fault.
It is not — it is the point. A fixed relationship between the subject and the
frame means the title always lands in the same place relative to the art, the
composition does not jump while scrolling, and 100 covers read as one designed
system instead of a scrapbook. Every platform UI enforces a rigid art spec for
exactly this reason. The consistency stays.

**3. Match the game's own tone.** Most were right — Mother 3's sunflowers,
Battle Network's neon grid, Minish Cap's forest. Advance Wars 2 was not: a
grim grey battlefield for a bright, comedic, cartoon-military game.

---

## The prompt

```
Extend and clean this Game Boy Advance box art into a widescreen wallpaper.

SOURCE
This is the front cover of {GAME}. Preserve its characters, colour palette
and illustration style — the same artist's hand. Match the GAME'S OWN TONE: a
bright comedic game stays bright and comedic, a gothic one gothic, a cute one
cute. Do not default to dark epic fantasy.

WHEN FIDELITY AND LAYOUT CONFLICT, LAYOUT WINS
Many GBA covers put the subject dead centre, filling the frame. Such a
composition CANNOT be extended outward and still leave a quiet left half —
the subject is already there. In that case do not force it: RE-STAGE the
scene. Move the subject into the right half and build new environment around
it. Re-staging is expected and correct for centre-dominant covers.

What must survive re-staging: the characters themselves (recognisable and
on-model), the palette, the art style, and the mood. What may change: where
things sit, the camera angle, and how much environment surrounds them.

OUTPUT
Save as a PNG file. 16:9 landscape, at least 960x544 (larger is fine — it is
downscaled later). No borders, no frame, no letterbox bars, edge to edge.

It will be displayed on a 480x272 screen, so favour bold readable shapes over
fine detail: thin lines, small text and fine texture all disappear at that size.

FILENAME: name the file exactly after the ROM, e.g.
   Pokemon - Emerald Version (USA, Europe).png
Art is matched to games by filename. An approximate name is recoverable —
HeroForge can re-match and rename a whole folder — but an exact one needs no
tool at all.

REMOVE COMPLETELY
- the game's title, logo and all wordmarks
- the silver "GAME BOY ADVANCE" spine down the left edge
- the ESRB / PEGI rating badge
- publisher and developer logos (Nintendo, Konami, THQ, etc.)
- "Link It Up!", "Player's Choice", seals, starbursts, stickers, banners
- any text of any kind, in any language

EXTEND
The cover is roughly square; the output is widescreen. Paint new artwork
outward in the same style, continuing the scene naturally — environment, sky,
atmosphere. Do not mirror or repeat existing elements. Do not invent
characters or objects the original does not imply.

COMPOSITION
- The LEFT 55% must stay visually QUIET: open sky, mist, water, gradient,
  shadow, blurred distance. Low contrast, low detail, darker than the right.
  White text is printed over this region and must remain readable. Nothing
  with hard edges or bright highlights belongs there.
- The main subject sits in the RIGHT HALF.
- KEEP THE FRAMING CONSISTENT ACROSS ALL IMAGES. The subject should occupy a
  similar share of the frame every time, in a similar position. These are
  shelf items under fixed on-screen text, not standalone illustrations —
  a consistent spec is what makes the library feel coherent when scrolling.
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
mockups. No logos. No watermarks.
```

---

## Per-image notes for the regenerations

| Image | Verdict | What to ask for |
|---|---|---|
| **Advance Wars 2** | regenerate | Bright daylight, saturated, cartoon-military. Cheerful cel-shaded cast, on-model — round friendly faces, not realistic anime. Blue sky with clouds, green terrain. Remove the tall dark machine that isn't in the source. |
| **Pokémon Emerald** | regenerate | The re-staging was the right call — the source has Rayquaza dead centre and it could not have been extended. The fault is CONTRAST, not size: it has receded into the clouds and gone muddy. Keep it the same scale and position; make it read clearly — brighter green, cleaner silhouette, more separation from the sky behind it. |
| **Minish Cap** | regenerate | Link is small and sits in the bottom band. Make him ~30% larger and higher — matching the subject scale the other images use, not exceeding it. Keep the forest and the cel-shaded style, they are right. |
| **All other 9** | keep, re-run only for the band | Composition and tone are good. Only regenerate to remove the bottom bar. |

## Installing

Drop the PNGs into `PSP/GAME/GBAdhoc/hero/` on the memory stick. Nothing else
is required.

The emulator decodes a PNG the first time it shows that game, then writes a
`.565` beside it — the texture, ready to use — so every later visit is one
read with no decode at all. That happens lazily, one game at a time and only
for games actually looked at, so a large library never stalls at boot.

There is no need to convert anything by hand, and no reason to ask an image
generator for an exotic format.

## After regenerating

Check that no image has a horizontal seam near the bottom. That was the one
systematic defect and it is the easiest thing to verify at a glance.
