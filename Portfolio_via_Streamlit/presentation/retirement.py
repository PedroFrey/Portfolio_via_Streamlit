"""Simulador de aposentadoria.

- Filtros lazy: so recalcula ao clicar em "Aplicar" (via st.form).
- Primeira carga ja mostra a simulacao com valores padrao.
- Formatacao monetaria via babel.
- Grafico interativo em Plotly.
- session_state namespaced com prefixo "retirement_".
"""

from __future__ import annotations

from datetime import date

import plotly.graph_objects as go
import streamlit as st
from babel.numbers import format_currency

from Portfolio_via_Streamlit.observability import safe_page, track_event
from Portfolio_via_Streamlit.services.retirement_service import (
    resumo_da_simulacao,
    simular_aposentadoria,
)

_PREFIX = "retirement_"

DEFAULTS = {
    "idade_atual": 18,
    "idade_aposentadoria": 65,
    "expectativa_vida": 85,
    "renda_mensal": 1621,
    "retorno_real_anual": 4.0,
    "inflacao_anual": 5.0,
    "aporte_mensal": 324,
    "patrimonio_inicial": 0,
}


def _moeda(valor: float) -> str:
    return format_currency(valor, "BRL", locale="pt_BR")


def _params_iniciais() -> dict[str, object]:
    return {
        "idade_atual": DEFAULTS["idade_atual"],
        "idade_aposentadoria": DEFAULTS["idade_aposentadoria"],
        "expectativa_vida": DEFAULTS["expectativa_vida"],
        "valor_desejado_por_ano": DEFAULTS["renda_mensal"] * 12,
        "retorno_real_anual": DEFAULTS["retorno_real_anual"] / 100,
        "inflacao_anual": DEFAULTS["inflacao_anual"] / 100,
        "aporte_mensal": DEFAULTS["aporte_mensal"],
        "patrimonio": DEFAULTS["patrimonio_inicial"],
    }


def _render_form() -> tuple[bool, dict[str, object], list[dict[str, object]]]:
    qtd_eventos = st.sidebar.number_input(
        "Quantidade de eventos extraordinarios",
        min_value=0,
        max_value=20,
        value=0,
        step=1,
        key=f"{_PREFIX}qtd_eventos",
    )

    with st.sidebar.form(f"{_PREFIX}form"):
        idade_atual = st.number_input(
            "Idade atual", min_value=0, max_value=120, value=DEFAULTS["idade_atual"], step=1
        )
        idade_aposentadoria = st.number_input(
            "Idade para aposentadoria",
            min_value=idade_atual,
            max_value=120,
            value=DEFAULTS["idade_aposentadoria"],
            step=1,
        )
        expectativa_vida = st.number_input(
            "Expectativa de vida",
            min_value=idade_aposentadoria,
            max_value=150,
            value=DEFAULTS["expectativa_vida"],
            step=1,
        )
        renda_mensal = st.number_input(
            "Renda desejada na aposentadoria (por mes)",
            min_value=0,
            value=DEFAULTS["renda_mensal"],
            step=100,
        )
        retorno_real_anual = (
            st.number_input(
                "Retorno real esperado (% ao ano)",
                min_value=0.0,
                max_value=100.0,
                value=DEFAULTS["retorno_real_anual"],
                step=0.1,
            )
            / 100
        )
        inflacao_anual = (
            st.number_input(
                "Inflacao estimada (% ao ano)",
                min_value=0.0,
                max_value=100.0,
                value=DEFAULTS["inflacao_anual"],
                step=0.1,
            )
            / 100
        )
        aporte_mensal = st.number_input(
            "Aporte mensal ate aposentadoria",
            min_value=0,
            value=DEFAULTS["aporte_mensal"],
            step=100,
        )
        patrimonio_inicial = st.number_input(
            "Patrimonio inicial", min_value=0, value=DEFAULTS["patrimonio_inicial"], step=500
        )

        st.markdown("---")
        st.subheader("📅 Eventos extraordinarios")
        eventos: list[dict[str, object]] = []
        for i in range(qtd_eventos):
            st.markdown(f"**Evento {i + 1}**")
            data_evento = st.date_input(
                f"Data do evento {i + 1}", value=date(2035, 12, 1), key=f"{_PREFIX}data_{i}"
            )
            valor = st.number_input(
                f"Valor do evento {i + 1}", value=0.0, step=100.0, key=f"{_PREFIX}valor_{i}"
            )
            positivo = st.checkbox(
                "E um credito? (Receita)", value=True, key=f"{_PREFIX}positivo_{i}"
            )
            eventos.append(
                {
                    "data": data_evento.strftime("%Y-%m-%d"),
                    "valor": valor if positivo else -valor,
                }
            )

        submitted = st.form_submit_button("✅ Aplicar")

    params = {
        "idade_atual": idade_atual,
        "idade_aposentadoria": idade_aposentadoria,
        "expectativa_vida": expectativa_vida,
        "valor_desejado_por_ano": renda_mensal * 12,
        "retorno_real_anual": retorno_real_anual,
        "inflacao_anual": inflacao_anual,
        "aporte_mensal": aporte_mensal,
        "patrimonio": patrimonio_inicial,
    }
    return submitted, params, eventos


def _plot(df) -> go.Figure:  # noqa: ANN001 — df: pd.DataFrame
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["data"],
            y=df["patrimonio"],
            mode="lines",
            name="Patrimonio (R$)",
            line={"color": "#16a34a", "width": 2},
            hovertemplate="%{x|%b/%Y}<br>R$ %{y:,.0f}<extra></extra>",
        )
    )
    inicio_aposentadoria = df[df["fase"] == "Aposentadoria"]["data"].iloc[0]
    fig.add_vline(
        x=inicio_aposentadoria.timestamp() * 1000,
        line_dash="dash",
        line_color="#dc2626",
        annotation_text="Inicio da aposentadoria",
        annotation_position="top",
    )
    fig.update_layout(
        yaxis_tickprefix="R$ ",
        yaxis_tickformat=",.0f",
        xaxis_title="Ano",
        yaxis_title="Patrimonio acumulado",
        hovermode="x unified",
        margin={"l": 40, "r": 20, "t": 30, "b": 40},
        height=450,
    )
    return fig


@safe_page("retirement")
def retirement_app() -> None:
    st.title("💰 Simulador de Aposentadoria")
    st.sidebar.header("🧠 Dados do Usuario")

    if f"{_PREFIX}params" not in st.session_state:
        st.session_state[f"{_PREFIX}params"] = _params_iniciais()
        st.session_state[f"{_PREFIX}eventos"] = []

    submitted, params, eventos = _render_form()
    if submitted:
        st.session_state[f"{_PREFIX}params"] = params
        st.session_state[f"{_PREFIX}eventos"] = eventos
        track_event("retirement_simulation_applied", **params)

    df = simular_aposentadoria(
        st.session_state[f"{_PREFIX}params"], st.session_state[f"{_PREFIX}eventos"]
    )
    resumo = resumo_da_simulacao(df)

    st.subheader("📊 Evolucao do Patrimonio")
    st.plotly_chart(_plot(df), use_container_width=True)

    st.subheader("📢 Destaques")
    st.caption(
        f"Voce podera se aposentar em {resumo.ano_aposentadoria}, com um patrimonio "
        f"estimado de {_moeda(resumo.patrimonio_no_inicio_da_aposentadoria)}."
    )
    st.caption(f"Patrimonio maximo: {_moeda(resumo.patrimonio_maximo)}")
    st.caption(
        "Esse valor permitira uma renda mensal inicial de aproximadamente: "
        f"{_moeda(resumo.renda_mensal_inicial)}"
    )
    if resumo.ano_de_esgotamento is None:
        st.caption("Pela projecao, a cobertura financeira nao se esgotaria.")
    else:
        st.caption(
            f"Pela projecao, a cobertura financeira se esgotaria em {resumo.ano_de_esgotamento}."
        )

    st.subheader("📈 Evolucao dos dados")
    df_formatado = df.copy()
    df_formatado["data"] = df_formatado["data"].dt.strftime("%d/%m/%Y")
    for col in ("patrimonio", "aporte", "retirada"):
        df_formatado[col] = df_formatado[col].map(_moeda)
    st.dataframe(
        df_formatado[["data", "patrimonio", "fase", "aporte", "retirada"]].set_index("data"),
        use_container_width=True,
    )
