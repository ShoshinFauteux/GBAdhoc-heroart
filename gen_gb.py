"""Generate Game Boy / Game Boy Color hero masters from their box art.

    python gen_gb.py --dry-run          write the full prompts to prompts_gb_full/
    python gen_gb.py                    generate every missing master
    python gen_gb.py --only Crystal     just the entries whose title matches
    python gen_gb.py --force            regenerate even if the master exists

Needs `pip install google-genai pillow` and GEMINI_API_KEY in the environment.
Each call sends the cover (boxart-gb/<stem>.png) plus PROMPT-GB.md's prompt,
filled in from prompts_gb.json, and saves the returned image unchanged as
masters/<stem>.png.  build.py then debands, resizes and converts it exactly
like the GBA cards.

The generator is a tool, not a judge: LOOK at every master before building.
PROMPT.md's one systematic defect (a dark band along the bottom) is the first
thing to check, and a GB cover that was mostly logo can come back with the
logo redrawn.  --dry-run exists so the same prompts can be pasted into any
generator by hand instead.
"""
import argparse
import io
import json
import os
import re
import sys

HERE      = os.path.dirname(os.path.abspath(__file__))
QUEUE     = os.path.join(HERE, 'prompts_gb.json')
TEMPLATE  = os.path.join(HERE, 'PROMPT-GB.md')
BOXART    = os.path.join(HERE, 'boxart-gb')
MASTERS   = os.path.join(HERE, 'masters')
FULL      = os.path.join(HERE, 'prompts_gb_full')


def load_template():
    text = open(TEMPLATE, encoding='utf-8').read()
    m = re.search(r'## The prompt\s+```\n(.*?)```', text, re.S)
    if not m:
        sys.exit('PROMPT-GB.md: no fenced prompt under "## The prompt"')
    return m.group(1)


def fill(template, entry):
    note = entry.get('note', '').strip()
    prompt = (template.replace('{CONSOLE}', entry['console'])
                      .replace('{GAME}', entry['title'])
                      .replace('{GAME_NOTE}',
                               'GAME NOTE\n' + note if note else ''))
    return re.sub(r'\n{3,}', '\n\n', prompt)


def generate(client, model, prompt, cover_path):
    from google.genai import types
    from PIL import Image

    cover = Image.open(cover_path).convert('RGB')
    resp = client.models.generate_content(
        model=model,
        contents=[cover, prompt],
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(aspect_ratio='16:9')))
    for cand in resp.candidates or []:
        for part in (cand.content.parts if cand.content else []) or []:
            if getattr(part, 'inline_data', None) and part.inline_data.data:
                return Image.open(io.BytesIO(part.inline_data.data))
    raise RuntimeError('no image in the response (finish reason: %s)' %
                       [c.finish_reason for c in resp.candidates or []])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--only', default='')
    ap.add_argument('--model', default='gemini-3-pro-image-preview',
                    help='the 47 GBA masters are 1376x768, which is this '
                         "model's 16:9 output; gemini-2.5-flash-image also works")
    args = ap.parse_args()

    template = load_template()
    queue = json.load(open(QUEUE, encoding='utf-8'))
    if args.only:
        queue = [e for e in queue if args.only.lower() in e['title'].lower()]

    missing = [e['stem'] for e in queue
               if not os.path.isfile(os.path.join(BOXART, e['stem'] + '.png'))]
    if missing:
        sys.exit('no cover in boxart-gb/ for: ' + ', '.join(missing))

    if args.dry_run:
        os.makedirs(FULL, exist_ok=True)
        for e in queue:
            with open(os.path.join(FULL, e['stem'] + '.txt'), 'w',
                      encoding='utf-8') as f:
                f.write(fill(template, e))
        print('%d prompts written to %s' % (len(queue), FULL))
        return 0

    if not os.environ.get('GEMINI_API_KEY'):
        sys.exit('GEMINI_API_KEY is not set (or use --dry-run and paste the '
                 'prompts into a generator by hand)')
    from google import genai
    client = genai.Client()
    os.makedirs(MASTERS, exist_ok=True)

    failed = 0
    for e in queue:
        out = os.path.join(MASTERS, e['stem'] + '.png')
        if os.path.exists(out) and not args.force:
            print('skip  %s (exists)' % e['title'])
            continue
        print('gen   %s ...' % e['title'], flush=True)
        try:
            img = generate(client, args.model, fill(template, e),
                           os.path.join(BOXART, e['stem'] + '.png'))
        except Exception as exc:  # report and keep going; one bad call is not the batch
            print('FAIL  %s: %s' % (e['title'], exc))
            failed += 1
            continue
        img.save(out)
        print('ok    %s  %dx%d' % (e['title'], img.width, img.height))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
