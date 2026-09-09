"""Camada de servico do simulador de aposentadoria.

Fina de proposito: valida a entrada crua (dict vindo dos widgets Streamlit)
contra os modelos Pydantic em ``domain.retirement`` e delega o calculo.
"""

from __future__ import annotations

import json
import time
from typing import Any

import pandas as pd
import streamlit as st

from Portfolio_via_Streamlit.domain.retirement import (
    RetirementEvent,
    RetirementParams,
    RetirementSimulationResult,
    simulate_retirement,
    summarize,
)
from Portfolio_via_Streamlit.logging_config import get_logger

log = get_logger(__name__)


@st.cache_data(show_spinner=False, ttl=600)
def _cached_simulate(params_json: str, events_json: str) -> pd.DataFrame:
    """Cache keyed pelos parametros serializados — evita recalcular a mesma
    simulacao a cada rerun do Streamlit quando nada relevante mudou.
    """
    params = RetirementParams.model_validate_json(params_json)
    events = [RetirementEvent.model_validate(e) for e in json.loads(events_json)]
    start = time.perf_counter()
    df = simulate_retirement(params, events)
    log.info(
        "retirement_simulation_executed",
        duracao_ms=round((time.perf_counter() - start) * 1000, 2),
        total_meses=len(df),
    )
    return df


def simular_aposentadoria(
    params: dict[str, Any],
    eventos_extraordinarios: list[dict[str, Any]] | None = None,
) -> pd.DataFrame:
    """API publica compativel com o codigo legado (recebe dicts)."""
    validated_params = RetirementParams.model_validate(params)
    validated_events = [RetirementEvent.model_validate(e) for e in (eventos_extraordinarios or [])]
    return _cached_simulate(
        validated_params.model_dump_json(),
        json.dumps([e.model_dump(mode="json") for e in validated_events]),
    )


def resumo_da_simulacao(df: pd.DataFrame) -> RetirementSimulationResult:
    """Wrapper fino para `domain.retirement.summarize`."""
    return summarize(df)
