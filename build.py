"""Build the installable hero pack from the masters.

    python build.py            masters/ -> build/{clean,480,565}
    python build.py --pack     ...and zip build/pack/ for a release

WHY THREE STAGES AND NOT ONE.  Each one exists because skipping it produced a
visible defect on a real console:

  1. DEBAND.  The v1 prompt asked for "the bottom 45 pixels calm and dark" and
     the generator obliged with a literal dark rectangle -- a flat step in
     luminance with a hard horizontal edge, in 10 of the first 12 images.  It
     reads as a letterbox bar rather than as artwork.  deband.py finds the
     step, divides the darkening back out to recover the pixels underneath,
     and re-applies it as a smooth ramp.  The darkening is wanted; the EDGE is
     the bug.

  2. RESIZE to 480x272, Lanczos, on the host.  The console would otherwise
     scale a 1376x768 texture down at draw time, every frame, forever.

  3. RGB565 with ordered dither.  The GE samples RGB565 either way -- the only
     question is where the 888->565 conversion happens.  Doing it here lets us
     dither it, which the console's straight truncation cannot, so skies and
     starfields come out visibly cleaner than the on-device path produces.
     The file IS the texture: loading it is one sceIoRead into the destination
     and nothing else.  Measured on the same image: 112 ms as PNG, 14 ms as
     .565.

Everything under build/ is reproducible from masters/ and is not committed.
"""
import os
import shutil
import sys
import zipfile

from PIL import Image

import deband
import raw565

MASTERS = 'masters'
OUT     = 'build'
W, H    = 480, 272


def main():
    if not os.path.isdir(MASTERS):
        print('no %s/ -- nothing to build' % MASTERS)
        return 2

    clean = os.path.join(OUT, 'clean')
    r480  = os.path.join(OUT, '480')
    r565  = os.path.join(OUT, '565')
    pack  = os.path.join(OUT, 'pack', 'hero')
    for d in (clean, r480, r565, pack):
        os.makedirs(d, exist_ok=True)

    names = sorted(f for f in os.listdir(MASTERS) if f.lower().endswith('.png'))
    print('%d masters\n' % len(names))
    for fn in names:
        stem = os.path.splitext(fn)[0]
        im = Image.open(os.path.join(MASTERS, fn)).convert('RGB')

        fixed, factor = deband.deband(im)
        fixed.save(os.path.join(clean, fn))

        small = fixed.resize((W, H), Image.LANCZOS)
        small.save(os.path.join(r480, fn))

        dst = os.path.join(r565, stem + '.565')
        n = raw565.convert(os.path.join(r480, fn), dst, True)

        # the pack ships BOTH: .565 for zero cost on first view, and the 480
        # PNG so anyone can see what it is, edit it, or re-bake it themselves.
        shutil.copyfile(dst, os.path.join(pack, stem + '.565'))
        shutil.copyfile(os.path.join(r480, fn), os.path.join(pack, fn))

        print('  %-52s %-14s %4d KB' %
              (stem[:52], 'deband x%.2f' % factor if factor else 'no seam',
               n // 1024))

    if '--pack' in sys.argv:
        zp = os.path.join(OUT, 'gbadhoc-heroart-%d-cards.zip' % len(names))
        with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
            for f in sorted(os.listdir(pack)):
                z.write(os.path.join(pack, f), os.path.join('hero', f))
            z.write('README.md')
        print('\n%s  (%.1f MB)' % (zp, os.path.getsize(zp) / 1048576.0))
    return 0


if __name__ == '__main__':
    sys.exit(main())
