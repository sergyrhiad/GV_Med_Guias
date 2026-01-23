import sys
from pathlib import Path
import io
import re

import fitz
from PIL import Image
import pytesseract

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.operators.unimed.template import TEMPLATE

def ocr_rect(page, rc, dpi=350):
    cfg = "--psm 7 -c tessedit_char_whitelist=0123456789/"
    r = fitz.Rect(*rc)
    pix = page.get_pixmap(clip=r, dpi=dpi)
    img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")
    img = img.point(lambda p: 255 if p > 180 else 0)
    raw = pytesseract.image_to_string(img, lang="por", config=cfg).strip()
    dig = re.sub(r"[^0-9]", "", raw)
    return raw, dig

def main():
    pdf = "data/input/unimed/img-600-ppp.pdf"
    doc = fitz.open(pdf)
    page = doc[0]

    # usamos o Y do template da senha como base, mas com altura maior (já vimos que precisa)
    x0, y0, x1, y1 = TEMPLATE["Senha"]
    h = 20  # aumenta a altura para capturar os dígitos no scan

    # janela fixa de largura (vamos mover ela no X)
    w = 180

    # varre o X em passos de 20 pontos
    print("Varrendo X... (mostrando só quando achar 8+ dígitos)")
    for start_x in range(250, 750, 20):
        rc = (start_x, y0, start_x + w, y1 + h)
        raw, dig = ocr_rect(page, rc)

        # mostra só tentativas "promissoras" (muitos dígitos)
        if len(dig) >= 8:
            print("x=", start_x, "rect=", tuple(round(v,2) for v in rc), "digits=", dig, "raw=", repr(raw))

if __name__ == "__main__":
    main()
