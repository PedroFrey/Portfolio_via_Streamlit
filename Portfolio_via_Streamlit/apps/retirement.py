import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from datetime import date
from Portfolio_via_Streamlit.services.retirement_service import simular_aposentadoria


def formatar_valor(x, _):
    return f'R$ {x:,.0f}'.replace(",", ".")


def formatar_moeda(valor):
    if valor is None:
        return ""
    return f'R$ {valor:,.2f}'.replace(",", "X").replace(".", ",").replace("X", ".")


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


def retirement_app():
    st.title("💰 Simulador de Aposentadoria")
    st.sidebar.header("🧠 Dados do Usuário")

    # Na primeira carga, popula session_state com os valores padrão
    if "params" not in st.session_state:
        st.session_state["params"] = {
            "idade_atual": DEFAULTS["idade_atual"],
            "idade_aposentadoria": DEFAULTS["idade_aposentadoria"],
            "expectativa_vida": DEFAULTS["expectativa_vida"],
            "valor_desejado_por_ano": DEFAULTS["renda_mensal"] * 12,
            "retorno_real_anual": DEFAULTS["retorno_real_anual"] / 100,
            "inflacao_anual": DEFAULTS["inflacao_anual"] / 100,
            "aporte_mensal": DEFAULTS["aporte_mensal"],
            "patrimonio": DEFAULTS["patrimonio_inicial"],
        }
        st.session_state["eventos"] = []

    # qtd_eventos fica FORA do form: precisa reagir na hora
    # para desenhar os campos certos de cada evento
    qtd_eventos = st.sidebar.number_input(
        "Quantidade de eventos extraordinários", min_value=0, max_value=20, value=0, step=1
    )

    with st.sidebar.form("filtros_form"):
        idade_atual = st.number_input("Idade atual", min_value=0, max_value=120, value=DEFAULTS["idade_atual"], step=1)
        idade_aposentadoria = st.number_input("Idade para aposentadoria", min_value=idade_atual, max_value=120, value=DEFAULTS["idade_aposentadoria"], step=1)
        expectativa_vida = st.number_input("Expectativa de vida", min_value=idade_aposentadoria, max_value=150, value=DEFAULTS["expectativa_vida"], step=1)
        renda_mensal = st.number_input("Renda desejada na aposentadoria (por mês)", min_value=0, value=DEFAULTS["renda_mensal"], step=100)
        retorno_real_anual = st.number_input("Retorno real esperado (% ao ano)", min_value=0.0, max_value=100.0, value=DEFAULTS["retorno_real_anual"], step=0.1) / 100
        inflacao_anual = st.number_input("Inflação estimada (% ao ano)", min_value=0.0, max_value=100.0, value=DEFAULTS["inflacao_anual"], step=0.1) / 100
        aporte_mensal = st.number_input("Aporte mensal até aposentadoria", min_value=0, value=DEFAULTS["aporte_mensal"], step=100)
        patrimonio_inicial = st.number_input("Patrimônio inicial", min_value=0, value=DEFAULTS["patrimonio_inicial"], step=500)

        st.markdown("---")
        st.subheader("📅 Eventos extraordinários")
        eventos = []
        for i in range(qtd_eventos):
            st.markdown(f"**Evento {i+1}**")
            data_evento = st.date_input(f"Data do evento {i+1}", value=date(2035, 12, 1), key=f"data_{i}")
            valor = st.number_input(f"Valor do evento {i+1}", value=0.0, step=100.0, key=f"valor_{i}")
            positivo = st.checkbox("É um crédito? (Receita)", value=True, key=f"positivo_{i}")
            valor_final = valor if positivo else -valor
            eventos.append({
                "data": data_evento.strftime('%Y-%m-%d'),
                "valor": valor_final
            })

        renda_desejada_por_ano = renda_mensal * 12

        submitted = st.form_submit_button("✅ Aplicar")

    if submitted:
        st.session_state["params"] = {
            "idade_atual": idade_atual,
            "idade_aposentadoria": idade_aposentadoria,
            "expectativa_vida": expectativa_vida,
            "valor_desejado_por_ano": renda_desejada_por_ano,
            "retorno_real_anual": retorno_real_anual,
            "inflacao_anual": inflacao_anual,
            "aporte_mensal": aporte_mensal,
            "patrimonio": patrimonio_inicial,
        }
        st.session_state["eventos"] = eventos

    df = simular_aposentadoria(st.session_state["params"], eventos_extraordinarios=st.session_state["eventos"])

    # Plotar gráfico
    st.subheader("📊 Evolução do Patrimônio")
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.plot(df["data"], df["patrimonio"], label="Patrimônio (R$)", linewidth=2, color='green')

    aposentadoria_inicio = df[df["fase"] == "Aposentadoria"]["data"].iloc[0]
    ax.axvline(x=aposentadoria_inicio, color='red', linestyle="--", label="Início da aposentadoria")

    ax.yaxis.set_major_formatter(FuncFormatter(formatar_valor))
    ax.set_xticks(df["data"][::12])
    ax.set_xticklabels(df["ano"][::12], rotation=90)
    ax.set_xlabel("Ano")
    ax.set_ylabel("Patrimônio acumulado")

    ax.legend()
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.4)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_alpha(0.75)
    ax.spines['bottom'].set_alpha(0.75)
    st.pyplot(fig)

    # Formatar tabela
    df_formatado = df.copy()
    df_formatado["data"] = df_formatado["data"].dt.strftime('%d/%m/%Y').fillna("")
    colunas_monetarias = ["patrimonio", "aporte", "retirada"]
    for col in colunas_monetarias:
        df_formatado[col] = df_formatado[col].map(formatar_moeda)

    # Exibir Destaques
    st.subheader("📢 Destaques")
    ano_aposentadoria = df[df["fase"] == "Aposentadoria"]["data"].min().strftime('%Y')
    patrimonio_inicio_aposentadoria = df[df["fase"] == "Crescimento"]["patrimonio"].max()
    st.caption(f'Você poderá se aposentar em {ano_aposentadoria}, com um patrimônio estimado de R${patrimonio_inicio_aposentadoria:,.2f}.')
    patrimonio_maximo = df["patrimonio"].max()
    st.caption(f'Patrimônio máximo: R${patrimonio_maximo:,.2f}')
    renda_inicial = df.retirada[df.fase == "Aposentadoria"].min()
    st.caption(f'Esse valor permitirá uma renda mensal inicial de aproximadamente: R${renda_inicial:,.2f}')

    data_perda = df.data[(df.fase == "Aposentadoria") & (df.patrimonio == 0)].min()
    if data_perda is None or str(data_perda) == "NaT":
        final_da_frase = "não se esgotaria."
    else:
        data_perda = data_perda.strftime('%Y')
        final_da_frase = f'se esgotaria em {data_perda}.'
    st.caption(f'Pela projeção, a cobertura financeira {final_da_frase}')

    # Exibir tabela
    st.subheader("📈 Evolução dos dados")
    st.dataframe(df_formatado[["data", "patrimonio", "fase", "aporte", "retirada"]].set_index("data"))
