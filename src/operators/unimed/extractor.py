import fitz  # PyMuPDF
import re

# Importa funções utilitárias (limpar texto e pegar só dígitos)
from src.core.text_utils import clean, only_digits

# Importa o template com as regiões fixas do PDF
from src.operators.unimed.template import TEMPLATE, SCANNED_OVERRIDES


def extract_clip_text(page, rect) -> str:
    """
    Extrai texto de uma região (retângulo) específica do PDF.
    page: objeto da página do PDF (PyMuPDF)
    rect: tupla (x0, y0, x1, y1)
    """
    # Converte a tupla em um retângulo do PyMuPDF
    r = fitz.Rect(*rect)

    # Pega o texto apenas dentro dessa área (clip)
    text = page.get_text("text", clip=r)

    # Normaliza espaços/quebras de linha
    return clean(text)

def ocr_clip_text(page, rect, dpi: int = 600) -> str:
    """
    Faz OCR (Tesseract) em uma região do PDF (útil para PDF escaneado, que não tem camada de texto).

    page: página do PyMuPDF
    rect: tupla (x0, y0, x1, y1)
    dpi: resolução usada para renderizar o recorte (quanto maior, melhor OCR; mais lento)
    """
    import io
    from PIL import Image
    import pytesseract

    # Converte a tupla em retângulo
    r = fitz.Rect(*rect)

    # Renderiza só o recorte como imagem
    pix = page.get_pixmap(clip=r, dpi=dpi)

    # Converte para PIL e aplica um pré-processamento simples
    img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")

    # Binarização leve para melhorar contraste no scan
    img = img.point(lambda p: 255 if p > 180 else 0)

    # OCR priorizando números e "/" (muito comum em datas/códigos)
    cfg = "--psm 7 -c tessedit_char_whitelist=0123456789/ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-"

    text = pytesseract.image_to_string(img, lang="por", config=cfg)

    # Normaliza espaços/quebras de linha
    return clean(text)


def parse_pdf(pdf_path: str) -> dict:
    """
    Abre o PDF e extrai os campos definidos no TEMPLATE.
    Retorna um dicionário com os campos extraídos.
    """
    # Abre o PDF
    doc = fitz.open(pdf_path)

    # Começar com a primeira página (índice 0)
    page = doc[0]

    fields = {}

    # Detecta se a página tem texto real (PDF digital) ou se é escaneado (imagem)
    page_text = page.get_text("text").strip()
    is_scanned = (len(page_text) < 20)

    for field_name, rect in TEMPLATE.items():
        # Se for escaneado e existir retângulo ajustado, usa o override
        rect_to_use = rect
        if is_scanned and field_name in SCANNED_OVERRIDES:
            rect_to_use = SCANNED_OVERRIDES[field_name]

        if not is_scanned:
            fields[field_name] = extract_clip_text(page, rect_to_use)
        else:
            fields[field_name] = ocr_clip_text(page, rect_to_use)

    # -----------------------------
    # Normalizações úteis
    # (garantir que campos numéricos fiquem só com dígitos)
    # -----------------------------
    fields["GuiaPrestador"] = only_digits(fields.get("GuiaPrestador", ""))
    fields["Senha"] = only_digits(fields.get("Senha", ""))
    fields["GuiaOperadora"] = only_digits(fields.get("GuiaOperadora", ""))
    fields["Codigo"] = only_digits(fields.get("Codigo", ""))
    fields["Quantidade"] = only_digits(fields.get("Quantidade", ""))
    fields["Quantidade28"] = only_digits(fields.get("Quantidade28", ""))
    
    # -----------------------------
    # Campo 14 - Nome do Contratado (Cadastro)
    # -----------------------------
    raw_contratado = fields.get("NomeContratadoCadastro", "")
    raw_contratado = clean(raw_contratado)

    # Campo 15 - Profissional Solicitante
    prof = clean(fields.get("ProfissionalSolicitante", ""))
    cut = prof.lower().find("dados da")
    if cut != -1:
        prof = prof[:cut].strip()
    fields["ProfissionalSolicitante"] = prof

    # Campo 16 - Conselho
    fields["ConselhoProfissional"] = clean(fields.get("ConselhoProfissional", ""))

    # Campo 17 - Número do conslho (só dígitos)
    fields["NrConselho"] = only_digits(fields.get("NrConselho", ""))

    # Campo 18 - UF
    fields["Estado"] = (fields.get("Estado", "") or "").strip().upper()

    # Campo 19 - CBOS (só dígitos)
    fields["CBOS"] = only_digits(fields.get("CBOS", ""))

    # Padrão comum: "xxxx - yyyyyy NOME COMPLETO"
    m = re.match(r"^\s*\d+\s*-\s*\d+\s+(.*)$", raw_contratado)
    if m:
        fields["NomeContratadoCadastro"] = m.group(1).strip()
    else:
        # fallback: remove um prefixo numérico simples, se existir
        fields["NomeContratadoCadastro"] = re.sub(r"^\s*\d+\s+", "", raw_contratado).strip()

    # Prioridade: Campo 42 (Quantidade) > Campo 27 (Quantidade27)
    if not fields.get("Quantidade"):
        fields["Quantidade"] = fields.get("Quantidade28", "")
    
    return fields
