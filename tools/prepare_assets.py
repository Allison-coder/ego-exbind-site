"""Render user-supplied PDF figures; never modify the source files."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

import fitz
from PIL import Image

FIGURES = {
    "actions": "fig_2_1_ek100_verb_noun_actions.pdf",
    "overview": "fig_3_1_egoexbind_overview.pdf",
    "retrieval": "fig1_retrieval_pretraining_exposure.pdf",
    "binding": "fig_binding_exposure.pdf",
    "pmi": "fig_pmi_retrieval (3).pdf",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--only", choices=FIGURES)
    args = parser.parse_args()
    target = Path(__file__).resolve().parents[1] / "assets" / "figures"
    target.mkdir(parents=True, exist_ok=True)
    manifest_path = target / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else []
    for name, filename in FIGURES.items():
        if args.only and name != args.only:
            continue
        source = args.source / filename
        with fitz.open(source) as doc:
            page = doc[0]
            scale = 2400 / page.rect.width
            pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
            image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
            image.save(target / (name + ".webp"), "WEBP", quality=95, method=6)
            shutil.copyfile(source, target / (name + ".pdf"))
            if name == "retrieval":
                (target / "retrieval.svg").write_text(page.get_svg_image(text_as_path=True), encoding="utf-8")
            manifest = [entry for entry in manifest if entry["id"] != name]
            manifest.append({"id": name, "source": filename,
                             "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                             "width": pixmap.width, "height": pixmap.height})
    (target / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
