import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os
import getpass

# cache para não duplicar handlers quando importar
_LOGGERS = {}


def get_logger(name: str, operator: str = "app", user: str | None = None) -> logging.LoggerAdapter:

    # Cria um logger e Retorna LoggerAdapter

    project_root = Path(__file__).resolve().parents[2]  # raiz do projeto
    logs_dir = project_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Usuário padrão do Windows
    if user is None:
        user = os.getenv("USERNAME") or getpass.getuser() or "unknown"

    key = f"{operator}:{name}:{user}"
    if key in _LOGGERS:
        return _LOGGERS[key]

    logger = logging.getLogger(f"{operator}.{name}")
    logger.setLevel(logging.INFO)

    # Evita duplicar handlers se o Python recarregar/importar várias vezes
    if not logger.handlers:
        log_file = logs_dir / f"{operator}.log"

        # Rotação: 2 MB por arquivo, guarda 5 arquivos antigos
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=2_000_000,
            backupCount=5,
            encoding="utf-8"
        )

        # Formato: data/hora | nível | user | operator | logger | mensagem
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | user=%(user)s | op=%(op)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    adapter = logging.LoggerAdapter(logger, extra={"user": user, "op": operator})
    _LOGGERS[key] = adapter
    return adapter
