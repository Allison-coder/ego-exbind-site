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
    "retrieval": "fig_zero_shot_retrieval_exposure (1).pdf",
    "binding": "fig_binding_exposure.pdf",
    "pmi": "fig_pmi_retrieval (3).pdf",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    target = Path(__file__).resolve().parents[1] / "assets" / "figures"
    target.mkdir(parents=True, exist_ok=True)
    manifest = []
    for name, filename in FIGURES.items():
        source = args.source / filename
        with fitz.open(source) as doc:
            page = doc[0]
            scale = 2400 / page.rect.width
            pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
            image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
            image.save(target / (name + ".webp"), "WEBP", quality=95, method=6)
            shutil.copyfile(source, target / (name + ".pdf"))
            manifest.append({"id": name, "source": filename,
                             "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                             "width": pixmap.width, "height": pixmap.height})
    (target / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
