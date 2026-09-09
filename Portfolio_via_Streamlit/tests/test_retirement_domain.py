"""Testes da logica pura de simulacao de aposentadoria."""

from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from pydantic import ValidationError

from Portfolio_via_Streamlit.domain.retirement import (
    RetirementEvent,
    RetirementParams,
    simulate_retirement,
    summarize,
)


def test_idades_fora_de_ordem_sao_rejeitadas() -> None:
    with pytest.raises(ValidationError):
        RetirementParams(
            idade_atual=70,
            idade_aposentadoria=65,
            expectativa_vida=85,
            valor_desejado_por_ano=12000,
            retorno_real_anual=0.04,
            inflacao_anual=0.05,
        )


def test_retorno_negativo_e_rejeitado() -> None:
    with pytest.raises(ValidationError):
        RetirementParams(
            idade_atual=30,
            idade_aposentadoria=65,
            expectativa_vida=85,
            valor_desejado_por_ano=12000,
            retorno_real_anual=-0.01,
            inflacao_anual=0.05,
        )


@pytest.fixture
def params_exemplo() -> RetirementParams:
    return RetirementParams(
        idade_atual=30,
        idade_aposentadoria=65,
        expectativa_vida=85,
        valor_desejado_por_ano=12000,
        retorno_real_anual=0.04,
        inflacao_anual=0.05,
        aporte_mensal=500,
        patrimonio=0,
    )


def test_simulacao_gera_uma_linha_por_mes(params_exemplo: RetirementParams) -> None:
    df = simulate_retirement(params_exemplo)
    meses_totais = (65 - 30 + 85 - 65) * 12
    assert len(df) == meses_totais


def test_fase_crescimento_antes_da_aposentadoria(params_exemplo: RetirementParams) -> None:
    df = simulate_retirement(params_exemplo)
    meses_ate_aposentar = (65 - 30) * 12
    assert (df.iloc[:meses_ate_aposentar]["fase"] == "Crescimento").all()
    assert (df.iloc[meses_ate_aposentar:]["fase"] == "Aposentadoria").all()


def test_patrimonio_cresce_durante_a_fase_de_acumulacao(
    params_exemplo: RetirementParams,
) -> None:
    df = simulate_retirement(params_exemplo)
    crescimento = df[df["fase"] == "Crescimento"]["patrimonio"]
    assert crescimento.is_monotonic_increasing


def test_evento_extraordinario_positivo_aumenta_patrimonio_no_mes(
    params_exemplo: RetirementParams,
) -> None:
    df_sem_evento = simulate_retirement(params_exemplo)
    evento = RetirementEvent(data=df_sem_evento.iloc[5]["data"].date(), valor=10_000)
    df_com_evento = simulate_retirement(params_exemplo, events=[evento])
    assert df_com_evento.iloc[5]["patrimonio"] > df_sem_evento.iloc[5]["patrimonio"]


def test_summarize_identifica_ano_de_aposentadoria(params_exemplo: RetirementParams) -> None:
    df = simulate_retirement(params_exemplo)
    resumo = summarize(df)
    assert resumo.patrimonio_maximo >= 0
    assert resumo.ano_aposentadoria.isdigit()


@given(
    idade_atual=st.integers(min_value=18, max_value=50),
    anos_ate_aposentar=st.integers(min_value=1, max_value=40),
    anos_de_aposentadoria=st.integers(min_value=1, max_value=30),
    retorno_real_anual=st.floats(min_value=0.0, max_value=0.15, allow_nan=False),
    inflacao_anual=st.floats(min_value=0.0, max_value=0.15, allow_nan=False),
    aporte_mensal=st.floats(min_value=0.0, max_value=5000.0, allow_nan=False),
    valor_desejado_por_ano=st.floats(min_value=0.0, max_value=200_000.0, allow_nan=False),
)
@settings(max_examples=50, deadline=None)
def test_patrimonio_nunca_fica_negativo(
    idade_atual: int,
    anos_ate_aposentar: int,
    anos_de_aposentadoria: int,
    retorno_real_anual: float,
    inflacao_anual: float,
    aporte_mensal: float,
    valor_desejado_por_ano: float,
) -> None:
    """Invariante de negocio: patrimonio nunca deve ficar negativo."""
    params = RetirementParams(
        idade_atual=idade_atual,
        idade_aposentadoria=idade_atual + anos_ate_aposentar,
        expectativa_vida=idade_atual + anos_ate_aposentar + anos_de_aposentadoria,
        valor_desejado_por_ano=valor_desejado_por_ano,
        retorno_real_anual=retorno_real_anual,
        inflacao_anual=inflacao_anual,
        aporte_mensal=aporte_mensal,
        patrimonio=0,
    )
    df = simulate_retirement(params)
    assert (df["patrimonio"] >= 0).all()
