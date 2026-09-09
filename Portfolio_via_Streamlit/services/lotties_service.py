"""Carregamento de animacoes Lottie locais."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st

from Portfolio_via_Streamlit.config import LOTTIES_DIR
from Portfolio_via_Streamlit.logging_config import get_logger

log = get_logger(__name__)


@st.cache_data(show_spinner=False)
def load_lottie(filename: str) -> dict[str, Any] | None:
    """Carrega um Lottie JSON local do diretorio LOTTIES_DIR."""
    path = Path(LOTTIES_DIR) / filename
    if not path.exists():
        log.warning("lottie_not_found", filename=filename)
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
