# Gallery previews

The gallery pages use checked-in progressive JPEG previews from
`images/previews/<color>/`. Each grid image's `data-full` attribute points to the
untouched original, which the lightbox loads on demand.

To regenerate previews after adding or replacing gallery originals:

```sh
python scripts/generate-gallery-previews.py
```

The maintenance script requires Pillow. There is no build step or additional
browser dependency; GitHub Pages serves the checked-in files directly. Add a new
gallery image with its preview `src`, original `data-full`, alt text, and
`loading="lazy"`, then regenerate previews before publishing.

Previews retain the full frame, apply EXIF orientation, and preserve the source
ICC color profile. They target 1280px width and at least 640px height where the
original allows it, without upscaling. This supports roughly 2x density for the
largest mobile card and the fixed-height desktop crop. JPEG quality is 85.
The original files are never rewritten.
