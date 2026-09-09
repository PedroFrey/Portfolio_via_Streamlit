"""Observabilidade: correlacao de sessao, error boundary por pagina, Sentry.

Streamlit nao expoe endpoints HTTP customizados nem um APM tradicional, entao
a estrategia aqui e: (1) todo log carrega um session_id de correlacao, (2)
toda pagina e protegida por um error boundary que loga o stacktrace completo
mas mostra uma mensagem amigavel ao usuario, (3) excecoes nao tratadas tambem
vao para o Sentry, se configurado.
"""

from __future__ import annotations

import functools
import time
from collections.abc import Callable
from typing import ParamSpec, TypeVar

import structlog

from Portfolio_via_Streamlit.config import settings
from Portfolio_via_Streamlit.logging_config import get_logger

log = get_logger(__name__)

P = ParamSpec("P")
R = TypeVar("R")

_SENTRY_INITIALIZED = False


def init_sentry() -> None:
    """Inicializa o Sentry SDK uma vez por processo, se SENTRY_DSN estiver setado."""
    global _SENTRY_INITIALIZED
    if _SENTRY_INITIALIZED or not settings.sentry_enabled:
        return

    import sentry_sdk

    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.environment,
        traces_sample_rate=0.2 if settings.environment == "production" else 1.0,
        send_default_pii=False,
    )
    _SENTRY_INITIALIZED = True
    log.info("sentry_initialized", environment=settings.environment)


def get_session_id() -> str:
    """Retorna um ID estavel de sessao do Streamlit para correlacionar logs."""
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        ctx = get_script_run_ctx()
        if ctx is not None:
            return ctx.session_id
    except Exception:  # nosec B110 — fallback intencional: sem ScriptRunContext (ex: testes)
        pass
    return "unknown-session"


def bind_session_context(page: str) -> None:
    """Vincula session_id e pagina atual a todos os logs subsequentes desta run."""
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(session_id=get_session_id(), page=page)


def safe_page(page_name: str) -> Callable[[Callable[P, R]], Callable[P, R | None]]:
    """Decorator de error boundary para funcoes de pagina Streamlit."""

    def decorator(func: Callable[P, R]) -> Callable[P, R | None]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
            bind_session_context(page_name)
            start = time.perf_counter()
            log.info("page_view", page=page_name)
            try:
                result = func(*args, **kwargs)
            except Exception as exc:  # noqa: BLE001 — boundary de topo, e intencional
                duration_ms = (time.perf_counter() - start) * 1000
                log.error(
                    "page_error",
                    page=page_name,
                    duration_ms=round(duration_ms, 2),
                    error=str(exc),
                    exc_info=True,
                )
                if settings.sentry_enabled:
                    import sentry_sdk

                    sentry_sdk.capture_exception(exc)

                import streamlit as st

                st.error(
                    "Algo deu errado ao carregar esta pagina. "
                    "O time ja foi notificado — tente novamente em instantes."
                )
                if settings.environment == "development":
                    st.exception(exc)
                return None
            else:
                duration_ms = (time.perf_counter() - start) * 1000
                log.info("page_rendered", page=page_name, duration_ms=round(duration_ms, 2))
                return result

        return wrapper

    return decorator


def track_event(event: str, **properties: object) -> None:
    """Loga um evento de produto e opcionalmente envia ao PostHog."""
    log.info("product_event", event_name=event, **properties)

    if not settings.analytics_enabled:
        return

    try:
        import posthog

        posthog.api_key = settings.posthog_api_key
        posthog.host = settings.posthog_host
        posthog.capture(distinct_id=get_session_id(), event=event, properties=properties)
    except Exception as exc:  # noqa: BLE001
        log.warning("analytics_event_failed", event=event, error=str(exc))
