# Mr. Reduction

16-bit rollcall SIG comparer: upload daily SIG PDFs, compare against a hard-wired final roster,
list closing stations and post reductions by borough, and export a PDF (1 post = 8 hrs/day = 40 HPW).

- `template.html` - the page (pdf.js + jsPDF/autotable from cdnjs). Placeholders are filled by `build.js`.
- `parser.js` - SIG text-layout parser (pdf.js text items -> station rows), shared by the build and the page.
- `src_art/` - SpriteCook-generated sprites, animations, background and icons.

The roster/sample data and the built HTML are deliberately NOT in this public repo (see `.gitignore`).
`build.js` expects the SIG PDFs, `baseline.json` and `run.js` alongside it in a private working folder.
