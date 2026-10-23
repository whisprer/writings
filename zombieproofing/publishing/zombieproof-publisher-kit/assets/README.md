Put your publisher's device here as `publisher-imprint.png`.

Use a transparent PNG with a little breathing room around the design. At the
default 25 mm printed width, 600 pixels across provides ample resolution.
JPEG and self-contained SVG also work: change `publisher.imprint_image` in
`publishing-details.json` to match the filename. SVG text uses local fonts;
convert lettering to paths in your design application for exact typography.

The image is placed on the title page and colophon. Its aspect ratio is
preserved. The cover carries the publisher's name as text. The complete cover
illustration from the supplied book is preserved.

To publish without an image, set `imprint_image` to `""`.

`sample-device.svg` is a clearly labelled demonstration used only by
`demo-details.json`. It is not your publisher's identity.
