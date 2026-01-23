from src.core.text_utils import only_digits

def apply_rules(fields: dict) -> dict:
    """
    Aplica regras de negócio da UNIMED em cima dos campos extraídos do PDF.

    - Campo 7 (GuiaOperadora) e Campo 5 (Senha) são a mesma informação:
    Se um vier vazio, copiamos do outro.
    - Campo 29/30 (CodOperadora / NomeContratadoExecucao) depende do procedimento (Codigo).
    - Quantidade: se vier vazio, assume 1.
    """

    # -----------------------------
    # 1) Senha <-> GuiaOperadora (fallback bidirecional)
    # -----------------------------
    senha = only_digits(fields.get("Senha", ""))
    guia_op = only_digits(fields.get("GuiaOperadora", ""))

    # Se a senha estiver vazia e a guia operadora tiver valor, copia
    if not senha and guia_op:
        senha = guia_op

    # Se a guia operadora estiver vazia e a senha tiver valor, copia
    if not guia_op and senha:
        guia_op = senha

    fields["Senha"] = senha
    fields["GuiaOperadora"] = guia_op

    # Se ambos existirem e forem diferentes, isso é suspeito (vale auditar)
    if senha and guia_op and senha != guia_op:
        fields["_warning"] = "Senha e GuiaOperadora vieram diferentes no PDF."

    # -----------------------------
    # 2) Regras do contratado (campo 29/30 do seu processo)
    # -----------------------------
    proc = only_digits(fields.get("Codigo", ""))

    if proc in {"40901106", "40901360"}:
        fields["CodOperadora"] = "109652"
        fields["NomeContratadoExecucao"] = "ALEXANDRE ROGINSKI MENDES DOS SANTOS"
    else:
        fields["CodOperadora"] = "116280"
        fields["NomeContratadoExecucao"] = "LUIZ FELIPE RAMOS GUBERT"

    # -----------------------------
    # 3) Quantidade default
    # -----------------------------
    if not fields.get("Quantidade"):
        fields["Quantidade"] = "1"

    # -----------------------------
    # 4) TipoAtendimento (Campo 32) e TipoConsulta (Campo 34)
    #
    # Regra:
    # - Se TipoAtendimento vier em branco: assume "23" (Exame)
    # - Se TipoAtendimento for "4" ou contiver "consulta":
    #       TipoConsulta = "1 - Primeira"
    # - Caso contrário:
    #       TipoConsulta = "" (fica em branco)
    #
    # Obs: TipoAtendimento pode vir do PDF (quando extrairmos) ou de FIXOS.
    # -----------------------------
    tipo_at_raw = (fields.get("TipoAtendimento") or "").strip()

    # Se vier em branco, aplica o padrão "23"
    if not tipo_at_raw:
        fields["TipoAtendimento"] = "23"
        tipo_at_raw = "23"
    else:
        # Mantém o valor como veio (ex.: "4", "4 - Consulta", "23", etc.)
        fields["TipoAtendimento"] = tipo_at_raw

    # Normalizações para checagem: texto em minúsculo e somente dígitos
    tipo_at_check = tipo_at_raw.lower()
    tipo_at_num = only_digits(tipo_at_check)

    # Define TipoConsulta apenas se for consulta
    if "consulta" in tipo_at_check or tipo_at_num == "4":
        fields["TipoConsulta"] = "1 - Primeira"
    else:
        fields["TipoConsulta"] = ""

    return fields