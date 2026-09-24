# Ego-ExBind project website

This is a standalone static website. It does not import, modify, or execute the
original research repository at https://github.com/Allison-coder/ego-exbind.
No package manager, build step, external font, or online model inference is needed.

## Preview

Open `index.html` in a browser. All assets use relative paths and work locally
or under the GitHub Pages project path `/ego-exbind-site/`.

## Publish separately

1. Create a NEW GitHub repository named `ego-exbind-site`.
2. Upload this directory's contents (not its enclosing folder). Keep `index.html`
   in the repository root. Include `assets/`, `styles.css`, `main.js`, and `.nojekyll`.
3. In the NEW repository, choose Settings > Pages > Deploy from a branch.
4. Select `main` and `/(root)`, then Save.
5. After a successful deployment, the expected address is
   https://Allison-coder.github.io/ego-exbind-site/.

This website has NOT been uploaded or published by its creation process.
Before publishing, confirm review anonymity requirements and permission to
redistribute the EPIC-KITCHENS example images. A public project page is not anonymous.

## Scientific provenance and limits

- The five PDF assets are exact copies of the user-provided files.
  `assets/figures/manifest.json` contains source filenames, checksums and preview sizes.
- WebP previews are PDF renders, not AI-generated or reconstructed scientific images.
  Rendering at a higher pixel count does not recover details missing in a raster PDF.
- Action captions follow dissertation Fig. 2.1: slice chilli, clean pan, squeeze lemon.
  These are illustrative frames, not new sample-level model predictions.
- The SC/UC/UA counts (8648/713/307) refer to 9668 retrieval queries.
- Frozen binding summaries (0.222 noun, 0.092 verb) are from dissertation Table 4.2,
  for 8592 eligible SC probes. These are not individual-example scores.
- Counterfactual values are transcribed from dissertation Table 4.6. No confidence
  intervals or per-example results were invented. Displayed deltas use the displayed
  rounded values and one reference, Zeroed.
- Counterfactual text follows the subsequently clarified protocol: backbone frozen
  during adapter/bias training; adapters and bias fixed during exposure replacement.
  Zeroed is NOT the original frozen zero-shot baseline.
- The supplied retrieval figure retains its original r=0.43 annotation unchanged.
  Check against full-precision logs before a final release; earlier discussion raised
  a rounding discrepancy. This build is not a fresh raw-data verification.
- The older sequential representation-intervention diagram and score-intervention
  diagram are intentionally not published in this first version: their interpretation
  needs alignment with the implemented experiment branches and checkpoint protocol.
- The generic VLP architecture figure is omitted because it is background rather
  than an original contribution; verify attribution before adding it.
- No author list, acceptance status, paper URL, or BibTeX has been guessed.

## Updating figures

Edit only this website directory. If necessary, regenerate preview assets with
`tools/prepare_assets.py SOURCE_DIRECTORY` using Python with PyMuPDF and Pillow.
The script writes into this website's `assets/figures/` directory only.

## Design and licenses

Layout inspiration: https://sid2697.github.io/epic-contact/.
The site's HTML, CSS and JavaScript are newly written; no reference-site code,
paper text, figures, meshes or data were copied.
Icons are from lucide-static 0.468.0; their license is in `assets/icons/LICENSE`.
Scientific figures and dataset media retain their respective rights and conditions.
