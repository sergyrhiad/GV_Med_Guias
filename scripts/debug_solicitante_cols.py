import sys
from pathlib import Path
import fitz

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.core.text_utils import clean


PDF_PATH = "data/input/unimed/exame_scaneado.pdf"

page = fitz.open(PDF_PATH)[0]


def find_header_rect(variants):
    """
    Encontra o retângulo (Rect) do título de uma coluna.
    A gente busca por várias variações do texto (com/sem acento).
    """
    for term in variants:
        rects = page.search_for(term)
        if rects:
            candidates = [r for r in rects if 120 <= r.y0 <= 160]
            best = candidates[0] if candidates else rects[0]
            return best
    return None


# Títulos das colunas
r16 = find_header_rect(["Conselho Profissional"])
r17 = find_header_rect(["Número no Conselho", "Numero no Conselho"])
r18 = find_header_rect(["UF"])
r19 = find_header_rect(["Código CBO", "Codigo CBO"])

if not all([r16, r17, r18, r19]):
    raise SystemExit("Não encontrei todos os títulos (16/17/18/19).")

# A linha de dados fica logo abaixo do maior y1 dos títulos
y0 = max(r16.y1, r17.y1, r18.y1, r19.y1) + 1
y1 = y0 + 14  # altura inicial

PAD16 = 35  # conselho
PAD17 = 20  # nro conselho
PAD18 = 12  # UF
PAD19 = 30  # CBOS

x16 = r16.x0 - PAD16
x17 = r17.x0 - PAD17
x18 = r18.x0 - PAD18
x19 = r19.x0 - PAD19

left = 21.75
right = page.rect.width - 21.75

rects = {
    "ProfissionalSolicitante": (left, y0, x16 - 2, y1),
    "ConselhoProfissional":    (x16, y0, x17 - 2, y1),
    "NrConselho":              (x17, y0, x18 - 2, y1),
    "Estado":                  (x18, y0, x19 - 2, y1),
    "CBOS":                    (x19, y0, right, y1),
}

print("=== COORDENADAS SUGERIDAS (x0, y0, x1, y1) ===")
for k, v in rects.items():
    print(f"{k} = {v}")

print("\n=== TESTE: TEXTO EXTRAÍDO EM CADA RETÂNGULO ===")
for k, v in rects.items():
    txt = clean(page.get_text("text", clip=fitz.Rect(*v)))
    print(f"{k} => {repr(txt)}")