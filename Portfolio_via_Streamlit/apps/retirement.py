import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from datetime import date
import pandas as pd
from Portfolio_via_Streamlit.services.retirement_service import simular_aposentadoria

def retirement_app():

    st.title("💰 Simulador de Aposentadoria")

    st.sidebar.header("🧠 Dados do Usuário")
    idade_atual = st.sidebar.number_input("Idade atual", min_value=0, max_value=120, value=18, step=1)
    idade_aposentadoria = st.sidebar.number_input("Idade para aposentadoria", min_value=idade_atual, max_value=120, value=65, step=1)
    expectativa_vida = st.sidebar.number_input("Expectativa de vida", min_value=idade_aposentadoria, max_value=150, value=85, step=1)

    renda_mensal = st.sidebar.number_input("Renda desejada na aposentadoria (por mês)", min_value=0, value=1621, step=100)
    valor_desejado_por_ano = renda_mensal * 12

    retorno_real_anual = st.sidebar.number_input("Retorno real esperado (% ao ano)", min_value=0.0, max_value=100.0, value=4.0, step=0.1) / 100
    inflacao_anual = st.sidebar.number_input("Inflação estimada (% ao ano)", min_value=0.0, max_value=100.0, value=5.0, step=0.1) / 100
    
    # Aporte mensal default como 20% do salario
    aporte_mensal = st.sidebar.number_input("Aporte mensal até aposentadoria", min_value=0, value= int(renda_mensal * 0.2), step=100)
    patrimonio_inicial = st.sidebar.number_input("Patrimônio inicial", min_value=0, value=0, step=500)

    st.sidebar.markdown("---")
    st.sidebar.subheader("📅 Eventos extraordinários")
    qtd_eventos = st.sidebar.number_input("Quantidade de eventos", min_value=0, max_value=20, value=0, step=1)

    eventos = []
    for i in range(qtd_eventos):
        st.sidebar.markdown(f"**Evento {i+1}**")
        data = st.sidebar.date_input(f"Data do evento {i+1}", value=date(2035, 12, 1), key=f"data_{i}")
        valor = st.sidebar.number_input(f"Valor do evento {i+1}", value=0.0, step=100.0, key=f"valor_{i}")
        positivo = st.sidebar.checkbox(f"É um crédito? (Receita)", value=True, key=f"positivo_{i}")

        valor_final = valor if positivo else -valor
        eventos.append({
            "data": data.strftime('%Y-%m-%d'),
            "valor": valor_final
        })


    params = {
        "idade_atual": idade_atual,
        "idade_aposentadoria": idade_aposentadoria,
        "expectativa_vida": expectativa_vida,
        "valor_desejado_por_ano": valor_desejado_por_ano,
        "taxa_retirada_anual": 1.0,
        "retorno_real_anual": retorno_real_anual,
        "inflacao_anual": inflacao_anual,
        "aporte_mensal": aporte_mensal,
        "patrimonio": patrimonio_inicial,
    }

    df = simular_aposentadoria(params, eventos_extraordinarios=eventos)

    # Plotar gráfico
    st.subheader("📊 Evolução do Patrimônio")

    #Criar a curva de patrimonio verde
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.plot(df["data"], df["patrimonio"], label="Patrimônio (R$)", linewidth=2, color='green')
    
    #Marcar o inicio da aposentadoria comlinha vermelha
    aposentadoria_inicio = df[df["fase"] == "Aposentadoria"]["data"].iloc[0]
    ax.axvline(x=aposentadoria_inicio, color='red', linestyle="--", label="Início da aposentadoria")

    def formatar_valor(x, _):
        return f'R$ {x:,.0f}'.replace(",", ".")
    
    ax.yaxis.set_major_formatter(FuncFormatter(formatar_valor))
    ax.set_xticks(df["data"][::12])
    ax.set_xticklabels(df["ano"][::12], rotation=90)

    ax.set_xlabel("Ano")
    ax.set_ylabel("Patrimônio acumulado")
    
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
    # Exibir tabela
    # Formatar colunas numéricas para moeda
    df_formatado = df.copy()
    df_formatado["patrimonio"] = df_formatado["patrimonio"].map(lambda x: f'R$ {x:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."))
    df_formatado["aporte"] = df_formatado["aporte"].map(lambda x: f'R$ {x:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."))
    df_formatado["retirada"] = df_formatado["retirada"].map(lambda x: f'R$ {x:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."))
    df_formatado["data"] = df_formatado["data"].dt.strftime('%d/%m/%Y')
    
    # Exibir resumo
    st.subheader("📢 Destaques")
    Ano_Aposentadoria = df[df["fase"] == "Aposentadoria"]["data"].min().strftime('%Y')
    st.caption(f'Ano Aposentadoria: {Ano_Aposentadoria}')

    Patrimonio_maximo = df["patrimonio"].max()
    st.caption(f'Patrimônio máximo: R${Patrimonio_maximo:,.2f}')
    
    Patrimonio_inicio_aposentadoria = df[df["fase"] == "Crescimento"]["patrimonio"].max()
    st.caption(f'Patrimônio no Início da Aposentadoria: R${Patrimonio_inicio_aposentadoria:,.2f}')
    filtro = (df["fase"] == "Aposentadoria") & (df["patrimonio"] == 0)
    data_perda = df[filtro]["data"].min()

    if pd.notna(data_perda):
        Ano_perda_de_cobertura = data_perda.strftime('%Y')
    else:
      Ano_perda_de_cobertura = "Nunca perdeu cobertura"
    st.caption(f'Ano de iníco de perda de cobertura: {Ano_perda_de_cobertura}')


    st.subheader("📈 Evolução dos dados")
    st.dataframe(df_formatado[["data", "patrimonio", "fase", "aporte", "retirada"]].set_index("data"))
######### Fim Retirement App