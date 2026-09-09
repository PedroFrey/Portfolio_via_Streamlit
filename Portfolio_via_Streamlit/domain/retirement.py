"""Logica de dominio do simulador de aposentadoria.

Modulo puro: sem Streamlit, sem I/O, sem efeitos colaterais.
"""

from __future__ import annotations

from datetime import date

import pandas as pd
from pydantic import BaseModel, Field, model_validator


class RetirementEvent(BaseModel):
    """Um evento extraordinario (aporte ou retirada pontual) numa data especifica."""

    data: date
    valor: float = Field(description="Positivo = credito/receita; negativo = debito/despesa")


class RetirementParams(BaseModel):
    """Parametros de entrada da simulacao, ja validados."""

    idade_atual: int = Field(ge=0, le=120)
    idade_aposentadoria: int = Field(ge=0, le=120)
    expectativa_vida: int = Field(ge=0, le=150)
    valor_desejado_por_ano: float = Field(ge=0)
    retorno_real_anual: float = Field(ge=0, le=1, description="Fracao, ex: 0.04 = 4% a.a.")
    inflacao_anual: float = Field(ge=0, le=1)
    aporte_mensal: float | None = Field(default=None, ge=0)
    patrimonio: float = Field(default=0, ge=0)

    @model_validator(mode="after")
    def _valida_ordem_das_idades(self) -> RetirementParams:
        if not self.idade_atual <= self.idade_aposentadoria <= self.expectativa_vida:
            raise ValueError(
                "As idades devem seguir: idade_atual <= idade_aposentadoria <= expectativa_vida"
            )
        return self


class RetirementSimulationResult(BaseModel):
    """Metadados de destaque da simulacao, derivados do DataFrame mes-a-mes."""

    ano_aposentadoria: str
    patrimonio_no_inicio_da_aposentadoria: float
    patrimonio_maximo: float
    renda_mensal_inicial: float
    ano_de_esgotamento: str | None

    model_config = {"frozen": True}


def simulate_retirement(
    params: RetirementParams,
    events: list[RetirementEvent] | None = None,
    start: date | None = None,
) -> pd.DataFrame:
    """Simula a evolucao patrimonial mes a mes ate o fim da expectativa de vida."""
    events = events or []
    start = start or date.today()

    retorno_nominal_anual = (1 + params.retorno_real_anual) * (1 + params.inflacao_anual) - 1
    retorno_mensal = (1 + retorno_nominal_anual) ** (1 / 12) - 1
    inflacao_mensal = (1 + params.inflacao_anual) ** (1 / 12) - 1

    meses_ate_aposentar = (params.idade_aposentadoria - params.idade_atual) * 12
    meses_apos_aposentar = (params.expectativa_vida - params.idade_aposentadoria) * 12
    total_meses = meses_ate_aposentar + meses_apos_aposentar

    retirada_base_mensal = params.valor_desejado_por_ano / 12

    if params.aporte_mensal is not None:
        aporte = params.aporte_mensal
    elif meses_ate_aposentar > 0 and retorno_mensal > 0:
        aporte = (
            params.valor_desejado_por_ano
            * retorno_mensal
            / ((1 + retorno_mensal) ** meses_ate_aposentar - 1)
        )
    else:
        aporte = 0.0

    datas = pd.date_range(start=start, periods=total_meses, freq="MS")

    eventos_por_mes: dict[pd.Timestamp, float] = {}
    for evento in events:
        chave = pd.Timestamp(evento.data).replace(day=1)
        eventos_por_mes[chave] = eventos_por_mes.get(chave, 0.0) + evento.valor

    patrimonio = params.patrimonio
    linhas: list[dict[str, object]] = []

    for mes in range(total_meses):
        data_mes = datas[mes]
        fase = "Crescimento" if mes < meses_ate_aposentar else "Aposentadoria"

        patrimonio *= 1 + retorno_mensal

        if fase == "Crescimento":
            patrimonio += aporte
            aporte_mes, retirada_mes = aporte, 0.0
        else:
            inflacao_acumulada = (1 + inflacao_mensal) ** mes
            retirada_corrigida = retirada_base_mensal * inflacao_acumulada
            patrimonio -= retirada_corrigida
            aporte_mes, retirada_mes = 0.0, retirada_corrigida

        patrimonio += eventos_por_mes.get(data_mes, 0.0)
        patrimonio = max(patrimonio, 0.0)

        linhas.append(
            {
                "data": data_mes,
                "ano": data_mes.year,
                "mes_nome": data_mes.strftime("%b/%Y"),
                "patrimonio": patrimonio,
                "aporte": aporte_mes,
                "retirada": retirada_mes,
                "fase": fase,
            }
        )

    return pd.DataFrame(linhas)


def summarize(df: pd.DataFrame) -> RetirementSimulationResult:
    """Extrai os destaques (highlights) de um DataFrame gerado por ``simulate_retirement``."""
    aposentadoria = df[df["fase"] == "Aposentadoria"]
    crescimento = df[df["fase"] == "Crescimento"]

    esgotamento = aposentadoria[aposentadoria["patrimonio"] == 0]["data"].min()
    ano_esgotamento = None if pd.isna(esgotamento) else esgotamento.strftime("%Y")

    return RetirementSimulationResult(
        ano_aposentadoria=aposentadoria["data"].min().strftime("%Y"),
        patrimonio_no_inicio_da_aposentadoria=float(crescimento["patrimonio"].max())
        if not crescimento.empty
        else float(df["patrimonio"].iloc[0]),
        patrimonio_maximo=float(df["patrimonio"].max()),
        renda_mensal_inicial=float(aposentadoria["retirada"].min()),
        ano_de_esgotamento=ano_esgotamento,
    )
