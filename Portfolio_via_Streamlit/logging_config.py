"""Logging estruturado (JSON) via structlog.

Por que: `print()` espalhado pelo codigo antigo nao e pesquisavel, nao tem
nivel, e nao carrega contexto (qual sessao? qual pagina?). Logs em JSON no
stdout ja sao suficientes para o Render (que captura stdout) sem precisar
de infra extra.

Uso:
    from Portfolio_via_Streamlit.logging_config import get_logger
    log = get_logger(__name__)
    log.info("simulacao_executada", idade_atual=30, duracao_ms=42)
"""

from __future__ import annotations

import logging
import sys

import structlog

from Portfolio_via_Streamlit.config import settings

_CONFIGURED = False


def configure_logging() -> None:
    """Configura structlog + stdlib logging uma unica vez por processo."""
    global _CONFIGURED
    if _CONFIGURED:
        return

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
    )

    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if settings.environment == "development":
        renderer: structlog.types.Processor = structlog.dev.ConsoleRenderer()
    else:
        renderer = structlog.processors.JSONRenderer()

    structlog.configure(
        processors=[*shared_processors, renderer],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.log_level.upper(), logging.INFO)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    _CONFIGURED = True


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    configure_logging()
    return structlog.get_logger(name)
