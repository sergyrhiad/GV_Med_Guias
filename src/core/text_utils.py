import re

#Normaliza texto extraído do PDF
def clean(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())

#Mantém apenas dígitos (0-9)
def only_digits(s: str) -> str:
    return re.sub(r"\D+", "", s or "")
