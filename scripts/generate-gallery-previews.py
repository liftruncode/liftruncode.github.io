"""Regenerate checked-in gallery JPEGs. Requires Python and Pillow; no site runtime dependencies."""

from pathlib import Path
import re

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]


def main():
    sources = set()
    for page in ROOT.glob('*.html'):
        sources.update(re.findall(r'data-full="(images/[^\"]+)"', page.read_text(encoding='utf-8')))
    if not sources:
        raise SystemExit('No gallery data-full attributes found.')
    for source in sorted(sources):
        destination = ROOT / 'images/previews' / Path(source).relative_to('images')
        destination.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(ROOT / source) as original:
            image = ImageOps.exif_transpose(original)
            # Cover a 608px mobile card or 320px-tall desktop card at roughly 2x.
            # Keep the whole frame: mobile uses height:auto, desktop object-fit:cover.
            scale = min(1, max(1280 / image.width, 640 / image.height))
            size = (round(image.width * scale), round(image.height * scale))
            image = image.resize(size, Image.Resampling.LANCZOS).convert('RGB')
            image.save(destination, 'JPEG', quality=85, optimize=True,
                       progressive=True, icc_profile=original.info.get('icc_profile'))
    print(f'Generated {len(sources)} gallery previews.')


if __name__ == '__main__':
    main()
