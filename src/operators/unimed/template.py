# TEMPLATE UNIMED
TEMPLATE = {
    # Campo 2 - Guia Prestador (nº guia no prestador)
    "GuiaPrestador": (720.0, 5.0, 763.0, 20.0),

    # Campo 5 - Senha
    "Senha": (436.0, 35.0, 486.0, 48.0),

    # Campo 7 - Número da Guia atribuído pela Operadora
    # Extrair também para ter fallback caso a Senha venha vazia
    "GuiaOperadora": (596.0, 35.0, 647.0, 48.0),

    # Campo 15 - Nome do Profissional Solicitante
    "ProfissionalSolicitante": (21.75, 143.4490203857422, 318.5, 157.4490203857422),

    # Campo 16 - Conselho Profissional
    "ConselhoProfissional": (320.5, 143.4490203857422, 466.25, 157.4490203857422),

    # Campo 17 - Número no Conselho
    "NrConselho": (468.25, 143.4490203857422, 596.5, 157.4490203857422),

    # Campo 18 - UF
    "Estado": (598.5, 143.4490203857422, 616.75, 157.4490203857422),

    # Campo 19 - Código CBO (CBOS)
    "CBOS": (618.75, 143.4490203857422, 820.1381225585938, 157.4490203857422),

    # Campo 14 - Nome do Contratado (linha logo abaixo do cabeçalho)
    "NomeContratadoCadastro": (21.75, 119.20, 810.33, 135.74),

    # Campo 15/16/17/18/19 - Linha de dados do solicitante.
    "SolicitanteLinha": (21.75, 142.45, 810.33, 177.75),

    # Campo 22 - Data de Solicitação
    "DataSolicitacao": (347.0, 35.0, 392.5, 48.0),

    # Campo 25/40 - Código do Procedimento (dependendo do layout)
    "Codigo": (76.0, 202.0, 112.0, 214.0),

    # Campo 27 - Qtde. Solic. (usaremos como fallback quando o Campo 42 estiver vazio)
    "Quantidade28": (720.0, 197.0, 770.0, 214.0),

    # Campo 32 - Tipo de Atendimento
    "TipoAtendimento": (22.0, 299.0, 93.0, 311.8),

    # Campo 42 - Quantidade
    "Quantidade": (650, 190, 700, 220),

}

# Retângulos ajustados especificamente para PDF ESCANEADO (imagem),

SCANNED_OVERRIDES = {
    # Campo 5 - Senha (escaneado)
    "Senha": (435, 45, 495, 60),
}