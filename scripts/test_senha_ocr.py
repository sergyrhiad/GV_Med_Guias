import sys
from pathlib import Path
import io
import re

import fitz
from PIL import Image
import pytesseract

# garante que "src" seja importável
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.operators.unimed.template import TEMPLATE


def run(pdf_path: str):
    doc = fitz.open(pdf_path)
    page = doc[0]

    x0, y0, x1, y1 = TEMPLATE["Senha"]

    tests = [
    ("x1+80",  (x0, y0, x1 + 80,  y1 + 20)),
    ("x1+120", (x0, y0, x1 + 120, y1 + 20)),
    ("x1+160", (x0, y0, x1 + 160, y1 + 20)),
    ]

    # força OCR a focar em dígitos e "/" (datas às vezes aparecem)
    cfg = "--psm 7 -c tessedit_char_whitelist=0123456789/"

    print("Senha TEMPLATE =", (x0, y0, x1, y1))

    for name, rc in tests:
        r = fitz.Rect(*rc)
        pix = page.get_pixmap(clip=r, dpi=350)
        img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")

        # binarização simples (melhora OCR em scan)
        img = img.point(lambda p: 255 if p > 180 else 0)

        raw = pytesseract.image_to_string(img, lang="por", config=cfg).strip()
        digits = re.sub(r"[^0-9]", "", raw)

        print(name, "rect=", tuple(round(v, 2) for v in rc), "raw=", repr(raw), "digits=", repr(digits))


if __name__ == "__main__":
    run("data/input/unimed/img-600-ppp.pdf")
