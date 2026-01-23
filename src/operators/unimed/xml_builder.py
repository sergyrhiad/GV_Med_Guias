import xml.etree.ElementTree as ET
# ElementTree = biblioteca padrão do Python para montar XML com segurança
from xml.dom import minidom


def build_xml(fields: dict) -> str:
    """
    Monta o XML final a partir do dicionário 'fields'.
    Retorna uma string XML.
    """

    # Tag raiz do XML
    root = ET.Element("Guia")

    # Ordem das tags no XML (ajustável depois conforme o padrão oficial)
    tag_order = [
        "GuiaPrestador",
        "GuiaOperadora",
        "AtendimentoRN",
        "NomeContratadoCadastro",
        "ProfissionalSolicitante",
        "ConselhoProfissional",
        "NrConselho",
        "Estado",
        "CBOS",
        "CaraterAtendimento",
        "DataSolicitacao",
        "CodOperadora",
        "NomeContratadoExecucao",
        "TipoAtendimento",
        "IndicacaoAcidente",
        "TipoConsulta",
        "Data",
        "HoraInicial",
        "HoraFinal",
        "Tab",
        "Codigo",
        "Quantidade",
        "Via",
        "Tecnica",
    ]

    # Cria cada tag e preenche o valor
    for tag in tag_order:
        el = ET.SubElement(root, tag)
        el.text = fields.get(tag, "") or ""

    # Converte para bytes (xml “cru”)
    xml_bytes = ET.tostring(root, encoding="utf-8")

    # Pretty print com indentação (mais profissional)
    dom = minidom.parseString(xml_bytes)
    return dom.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")
