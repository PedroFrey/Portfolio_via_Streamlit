import pandas as pd
import streamlit as st
import plotly_express as px
import plotly.graph_objects as go
from plotly import data

#==========
# Informações Gerais
# Para Rodar no Navegador: python -m streamlit run Learning.py
# Depois é so ir salvando e atualizando o navegador
#===========

#Duas formas de digitar dados para tabelas
ListaDeDicionarios = [
    {"Nome":"Zé","Idade":32,"Cidade": "SP"},
    {"Nome":"Beto","Idade":31,"Cidade": "RS"},
    {"Nome":"Bill","Idade":34,"Cidade": "RJ"},
]
DicionarioDeListas = {
"Nome": ["Zé", "Beto", "Bill"],
"Idade":[32,31,34],
"Cidade":["SP","RS","RJ"],
"Vendas": [2500,3400,1345],
"Cores":['red','blue','white']
}

# Criar o dataframe
df = pd.DataFrame(DicionarioDeListas)
# df = data.gapminder().query("continent == 'Europe' and (year == 1952 or year == 2002)") # Dados maiores diretamente do plotly
df # Exibir tabela na página

# Configurações para fig1 que é um gráfico de barras
fig1 = px.bar( x=df.Nome,
              y=df.Idade, 
              title="Idade por nome",
              color=df.Cores,
              color_discrete_map={c: c for c in df.Cores}
              )

fig1.update_traces(textposition = "inside")
fig1.update_layout(
                    annotations=[dict(text="Este é o meu subtítulo aqui")],
                    showlegend=False,
                    xaxis_title = "Nome",
                   yaxis_title = None,
                   plot_bgcolor = None,
                   yaxis=dict(showgrid = False),
                   
)
fig1

# Configurações para fig2 que é um histograma
fig2 = px.histogram(x=df.Cidade,y=df.Vendas, title="Vendas por Cidade")
fig2
