import pandas as pd
from datetime import date

def simular_aposentadoria(params, inicio=date.today().strftime("%Y-%m-%d"), eventos_extraordinarios=[]):
    # Inflação e retorno
    retorno_real_anual = params["retorno_real_anual"]
    inflacao_anual = params["inflacao_anual"]

    # Cálculo correto do retorno nominal e inflação mensal
    retorno_nominal_anual = (1 + retorno_real_anual) * (1 + inflacao_anual) - 1
    # Conversão de taxa/inflação anual para taxa/inflação mensal equivalente
    r_mensal = (1 + retorno_nominal_anual) ** (1/12) - 1
    inflacao_mensal = (1 + inflacao_anual) ** (1/12) - 1

    # Períodos
    meses_ate_aposentar = (params["idade_aposentadoria"] - params["idade_atual"]) * 12
    meses_apos_aposentar = (params["expectativa_vida"] - params["idade_aposentadoria"]) * 12
    total_meses = meses_ate_aposentar + meses_apos_aposentar

    # Retirada base mensal (valor informado pelo usuário convertido de ano para mês)
    retirada_base_mensal = params["valor_desejado_por_ano"] / 12

    # Capital necessário (não usado diretamente, mas mantido para exibição)
    capital_necessario = params["valor_desejado_por_ano"] # / params["taxa_retirada_anual"]

    # Cálculo do aporte (se não fornecido)
    if params["aporte_mensal"] is None:
        aporte = capital_necessario * r_mensal / ((1 + r_mensal) ** meses_ate_aposentar - 1)
    else:
        aporte = params["aporte_mensal"]

    # Datas
    datas = pd.date_range(start=inicio, periods=total_meses, freq='MS')
    df = pd.DataFrame(index=range(total_meses))
    df["data"] = datas
    df["ano"] = df["data"].dt.year
    df["mes_nome"] = df["data"].dt.strftime("%b/%Y")

    # Eventos
    eventos_dict = {}
    if eventos_extraordinarios:
        for evento in eventos_extraordinarios:
            data_evento = pd.to_datetime(evento["data"]).replace(day=1)
            eventos_dict[data_evento] = eventos_dict.get(data_evento, 0) + evento["valor"]

    # Simulação
    patrimonio = params.get("patrimonio", 0)
    patrimonio_lista = []
    aporte_lista = []
    retirada_lista = []
    fase_lista = []

    for mes in range(total_meses):
        data_mes = datas[mes]
        fase = "Crescimento" if mes < meses_ate_aposentar else "Aposentadoria"

        # Crescimento do patrimônio
        patrimonio *= (1 + r_mensal)

        # Correção da retirada pela inflação acumulada
        inflacao_acumulada = (1 + inflacao_mensal) ** mes

        if fase == "Crescimento":
            patrimonio += aporte
            aporte_lista.append(aporte)
            retirada_lista.append(0)
        else:
            retirada_corrigida = retirada_base_mensal * inflacao_acumulada
            patrimonio -= retirada_corrigida
            retirada_lista.append(retirada_corrigida)
            aporte_lista.append(0)

        # Eventos extraordinários
        if data_mes in eventos_dict:
            patrimonio += eventos_dict[data_mes]

        # Evita patrimônio negativo
        patrimonio = max(patrimonio, 0)

        # Salvar no histórico
        patrimonio_lista.append(patrimonio)
        fase_lista.append(fase)

    # Construir DataFrame final
    df["patrimonio"] = patrimonio_lista
    df["aporte"] = aporte_lista
    df["retirada"] = retirada_lista
    df["fase"] = fase_lista
    df["aporte_mensal"] = aporte
    df["retirada_base_mensal"] = retirada_base_mensal
    df["capital_necessario"] = capital_necessario
    df["inflacao_anual"] = inflacao_anual
    df["retorno_real_anual"] = retorno_real_anual
    df["retorno_nominal_anual"] = retorno_nominal_anual

    return df

# --- Bloco para teste no terminal ---
if __name__ == "__main__":
    simular_aposentadoria()