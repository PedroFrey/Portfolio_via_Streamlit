"""Smoke tests de UI: cada pagina deve renderizar sem lancar excecao.

Usa ``streamlit.testing.v1.AppTest.from_file``, apontando para pequenos
scripts em ``page_scripts/`` que so importam e chamam a funcao da pagina.
``AppTest.from_function`` foi considerado primeiro, mas ele serializa
apenas o corpo literal da funcao via ``inspect.getsource`` -- nao resolve
closures nem imports do modulo que a envolve, entao falha com
``NameError`` para qualquer runner que nao seja 100% autocontido. Scripts
de arquivo sao a forma suportada e robusta de fazer isso.

Nota: como cada pagina e protegida por ``@safe_page``, uma excecao interna
vira um `st.error` amigavel em vez de propagar -- por isso aqui verificamos
tanto ``at.exception`` (erros nao capturados, ex: de import) quanto a
ausencia do texto de erro do boundary nos elementos renderizados.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

_SCRIPTS_DIR = Path(__file__).parent / "page_scripts"

PAGE_SCRIPTS = [
    "run_home.py",
    "run_portfolio.py",
    "run_price_comparator.py",
    "run_puxa_conversa.py",
    "run_retirement.py",
]


@pytest.mark.parametrize("script_name", PAGE_SCRIPTS)
def test_pagina_renderiza_sem_excecao(script_name: str) -> None:
    script_path = _SCRIPTS_DIR / script_name
    at = AppTest.from_file(str(script_path), default_timeout=15)
    at.run()

    assert not at.exception, f"{script_name} lancou excecao: {at.exception}"
    erro_boundary = [e for e in at.error if "Algo deu errado" in e.value]
    assert not erro_boundary, f"{script_name} caiu no error boundary: {erro_boundary}"
