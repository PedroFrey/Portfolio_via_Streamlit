
import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import wikipedia
import matplotlib.pyplot as plt
from PIL import Image
import requests
from streamlit_lottie import st_lottie
import urllib
from matplotlib.ticker import FuncFormatter
from datetime import date
from streamlit_elements import elements, mui
import random
# import streamlit.components.v1 as components

## My Portfolio Visual Assets
urllib.request.urlretrieve('https://raw.githubusercontent.com/PedroFrey/Portfolio_via_Streamlit/refs/heads/master/cash-management-dashboard.png', "cash-management-dashboard.png")
img_finacial = Image.open('cash-management-dashboard.png')

urllib.request.urlretrieve('https://raw.githubusercontent.com/PedroFrey/Portfolio_via_Streamlit/refs/heads/master/pmo.PNG', "pmo.png")
img_pmo = Image.open('pmo.png')

## Stocks App Assets
stocks = {
    'Technology': {
        "Apple Inc.": 'AAPL',
        'Microsoft Corporation': 'MSFT',
        'Alphabet Inc.': 'GOOGL'
    },
    'Food': {
        "McDonald's Corporation": 'MCD',
        'The Coca-Cola Company': 'KO',
        'Nestle S.A.': 'NSRGF'
    },
    'Retail': {
        "Walmart": 'WMT',
        'Amazon.com, Inc.': 'AMZN',
        'Target Corporation': 'TGT'
    }
    }

# Convert the dictionary to a DataFrame
# In this rewritten code, the result variable is initialized as an empty list, and then two nested for loops are used to iterate over the stocks dictionary.
# For each category in stocks, the code iterates over each company and ticker pair in the companies dictionary associated with that category. For each pair, a tuple
# (category, company, ticker) is appended to the result list.

result = []
for category, companies in stocks.items():
    for company, ticker in companies.items():
        result.append((category, company, ticker))
df = pd.DataFrame(result, columns=['Category', 'Company', 'Ticker'])

# Set a default start date and end date
end_date_default = datetime.date.today()
start_date_default = end_date_default - datetime.timedelta(days=30)

######### Inicio do Stock App
def stock_dashboard():
    
  ## Header Section
  st.title("Simple Stock Price App")

  ## Filters Section
  # Detemine the name of header of the filter section
  st.sidebar.header("User input Features")
  # Configure the first filter related to category of the stock
  selected_category = st.sidebar.selectbox("Category picker",df['Category'].unique().tolist())
  # Configure the second filter related to ticket of the stock
  selected_ticket = st.sidebar.selectbox("Stock picker",df.loc[df.Category == selected_category]['Ticker'].unique().tolist())
  # Get the name of the company for text purposes.
  selected_company = df.loc[df.Ticker == selected_ticket]['Company'].unique()[0]

  # Add the date range filter to the sidebar
  with st.sidebar:
      st.write("Date Range Filter")
      start_date = st.date_input("Start date", start_date_default)
      end_date = st.date_input("End date", end_date_default)

  ## Data grabing from Yahoo
  tickerData = yf.Ticker(selected_ticket)
  tickerDF = tickerData.history(period='1d',start= start_date ,end= end_date )

  ## Visual assets
  fig_close_open, ax1 = plt.subplots(nrows=1, ncols=1,figsize=(20,5))

  ax1.plot(tickerDF.index,tickerDF.Close,linestyle='-',color="#EB2842", label='Close')
  ax1.plot(tickerDF.index,tickerDF.Open,linestyle='--',color='#38EB28', label='Open' )
  ax1.legend()
  ax1.set_xlabel("Date")
  ax1.set_ylabel("Amount of Open & Close")
  ax1.set_title("Open & Close of Stock")

  fig_volume, ax1 = plt.subplots(nrows=1, ncols=1,figsize=(20,5))

  barplot = ax1.bar(x = tickerDF.index,
          height = tickerDF.Volume/1_000_000,
          width=0.8,
          color="#075f63",
          label='Volume')
  # Function to add Values to Barplot
  for bar in barplot:
      height = bar.get_height()
      if height!=0:
        ax1.text(bar.get_x() + bar.get_width()/2, height,
                f'{height:.2f}',
                horizontalalignment ='center',
                verticalalignment='bottom',
                rotation=0)

  ax1.legend()
  ax1.set_xlabel("Date")
  #ax1.set_ylabel("Volume divided 1.000.000")
  ax1.set_title("Volume of Stock")

  #Remove tick_ from y axis
  ax1.tick_params(axis='y', which='both', length=0)
  #Remove numbers from y axis
  ax1.set_yticklabels([])

  # Data Grabing from Wikipedia
  # search for the wikipedia page about the company

  try:
    summary_wiki = wikipedia.summary(selected_company,auto_suggest = False)
  except: 
    summary_wiki  = "There is no information available."
    # Section Native visuals
  with st.container():
    st.write("---")
    st.write(f"""
    Shown are the stock **closing price** and **volume** of {selected_company}! 
    """)
    # Get info of Company
    st.write(summary_wiki[:200])

    st.markdown(f"To learn more about the company visit> https://www.wikipedia.com/{selected_company}")
  # Divide de section into 2 columns

    left_column,right_column = st.columns(2)
    with left_column:
      st.write("""
      ## Closing price
      """)
      st.line_chart(tickerDF.Close)
    with right_column:
      st.write("""
      ## Volume traded
      """)
      st.line_chart(tickerDF.Volume)
      # # Section External visuals
  with st.container():
    st.write("---")
    st.write("""  External visuals! """)
    #ext_left_column,ext_right_column = st.columns(2)
    #with ext_left_column:
    st.pyplot(fig_close_open)
    st.write("---")
    st.pyplot(fig_volume)
######### Fim do Stock App
######### Inicio do My Portfolio
def portfolio_app():
    
  # Tab configurations
  #st.set_page_config(page_title="[My Name]'s Creative Showcase", page_icon=':computer:',layout='wide')

  def load_lottieurl(url: str):
      r = requests.get(url)
      if r.status_code != 200:
          return None
      return r.json()

  lottie_What_do_I_do = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_5tl1xxnz.json")
  lottie_server = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_rrqimc3f.json")

  # Header section of Page
  with st.container():
    st.subheader("Discover my Portfolio: P. Frey's Creative Showcase")

    st.write("# Explore my Work in data science with emphasis on data visualization and Get to Know Me Better")

    sub_string = """
    Welcome to my portfolio! My name is P. Frey and I am a data scientist with a passion for data visualization.
    As a data scientist, I have the skills to collect, process, and analyze complex data sets, but my specialization in
     data visualization allows me to present the insights and findings in a visually appealing and easy-to-understand format.
      In this portfolio, you will find a collection of my best work in data visualization, including various interactive dashboards,
       charts, and graphs. You will also learn more about my experience and skills in data science, including my proficiency
        in programming languages such as Python, my knowledge of statistical models and machine learning algorithms,
         and my ability to communicate complex data analysis to both technical and non-technical audiences.
          Whether you are interested in exploring my work or looking for a data scientist with a specialization in data visualization,
           I invite you to browse my portfolio and get to know me better.
    """

    st.write(sub_string)

  # Presentation section of Page
  with st.container():
    st.write("---")
    left_column,right_column = st.columns(2)
    with left_column:
      st.header("What do I do")
      st.write("##")
      sub_string2 = """
      As a data scientist with a focus on data visualization, my primary goal is to transform complex data sets into meaningful
       insights and actionable recommendations. I use a variety of tools and techniques to collect, process, and analyze data,
        including statistical models, machine learning algorithms, and data visualization tools.In addition to my technical skills,
         I have strong communication and presentation skills, allowing me to effectively communicate insights to both technical and 
         non-technical audiences. I am also committed to staying up-to-date with the latest trends and advancements in data science,
          continuously learning new techniques and technologies to improve the quality and accuracy of my work. Ultimately,
           my goal as a data scientist is to help organizations make data-driven decisions and achieve their strategic objectives.
            I am passionate about using data to solve complex problems and make a positive impact on society.
      """
      st.write(sub_string2)
      st.write("[View my GitHub profile>](https://github.com/PedroFrey)")
    with right_column:
      st_lottie(lottie_What_do_I_do, key = "What do I do Image")
      st.write(":computer:")
  # First Project Section
  with st.container():
    st.write("---")
    #st.write("My projects")
    st.write("##")
    image_column,text_column = st.columns((1,2))
    with image_column:
      st.image(img_finacial)
    with text_column:
      st.subheader("Data Visualization for Financial Analysis")
      st.write("Financial Insights Dashboard: A Comprehensive Analysis of [Company/Market/Industry]")
      st.markdown("[Explore Financial Insights Dashboard](https://www.google.com)")
  # Second Project Section
  with st.container():
    st.write("---")
    #st.write("My projects")
    st.write("##")
    image_column,text_column = st.columns((1,2))
    with image_column:
      st.image(img_pmo)
    with text_column:
      st.subheader(" Data Visualization for Project Management")
      st.write("Project Management Office (PMO) Dashboard: Real-Time Insights for [Project/Program/Portfolio] Performance")
      st.markdown("[Explore PMO Dashboard for Project Insights](https://app.powerbi.com/view?r=eyJrIjoiYWMyZTIxOTItNzk2Ni00N2Q3LWE4YmUtNGViMWE0NjE3NzFlIiwidCI6ImUyZjc3ZDAwLTAxNjMtNGNmNi05MmIwLTQ4NGJhZmY5ZGY3ZCJ9)")
  # Closing Section
  with st.container():
    st.write("---")
    st_lottie(lottie_server,height= 300, key = "Server")
    st.write("##")
    sub_string3 = """To get in touch with me or inquire about potential projects or collaborations,
     feel free to send me an email at [Your Email Address]. I am always open to connecting with others
      in my field and exploring new opportunities to apply my skills in data science and data visualization.
       Whether you have a specific project in mind or simply want to learn more about my experience and expertise,
        I look forward to hearing from you!)
    """
    st.write(sub_string3)
    st.markdown("[>](https://www.google.com)")
######### Fim do My Portfolio
######### Preparação para Retirement App
def simular_aposentadoria(params, inicio=date.today().strftime("%Y-%m-%d"), eventos_extraordinarios=[]):
    # Inflação e retorno
    retorno_real_anual = params["retorno_real_anual"]
    inflacao_anual = params["inflacao_anual"]

    # Cálculo correto do retorno nominal e inflação mensal
    retorno_nominal_anual = (1 + retorno_real_anual) * (1 + inflacao_anual) - 1
    r_mensal = (1 + retorno_nominal_anual) ** (1/12) - 1
    inflacao_mensal = (1 + inflacao_anual) ** (1/12) - 1

    # Períodos
    meses_ate_aposentar = (params["idade_aposentadoria"] - params["idade_atual"]) * 12
    meses_apos_aposentar = (params["expectativa_vida"] - params["idade_aposentadoria"]) * 12
    total_meses = meses_ate_aposentar + meses_apos_aposentar

    # Retirada base mensal (valor informado pelo usuário convertido de ano para mês)
    retirada_base_mensal = params["valor_desejado_por_ano"] / 12

    # Capital necessário (não usado diretamente, mas mantido para exibição)
    capital_necessario = params["valor_desejado_por_ano"] / params["taxa_retirada_anual"]

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
######### Inicio Retirement App
def retirement_app():
    st.title("💰 Simulador de Aposentadoria")

    st.sidebar.header("🧠 Dados do Usuário")

    idade_atual = st.sidebar.number_input("Idade atual", min_value=0, max_value=120, value=18, step=1)
    idade_aposentadoria = st.sidebar.number_input("Idade para aposentadoria", min_value=idade_atual, max_value=120, value=65, step=1)
    expectativa_vida = st.sidebar.number_input("Expectativa de vida", min_value=idade_aposentadoria, max_value=150, value=85, step=1)

    valor_desejado_por_mes = st.sidebar.number_input("Renda desejada na aposentadoria (por mês)", min_value=0, value=1500, step=100)
    valor_desejado_por_ano = valor_desejado_por_mes * 12

    retorno_real_anual = st.sidebar.number_input("Retorno real esperado (% ao ano)", min_value=0.0, max_value=100.0, value=4.0, step=0.1) / 100
    inflacao_anual = st.sidebar.number_input("Inflação estimada (% ao ano)", min_value=0.0, max_value=100.0, value=5.0, step=0.1) / 100

    aporte_mensal = st.sidebar.number_input("Aporte mensal até aposentadoria", min_value=0, value=300, step=100)
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

    fig, ax = plt.subplots(figsize=(15, 6))
    ax.plot(df["data"], df["patrimonio"], label="Patrimônio (R$)", linewidth=2, color='green')

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
    st.subheader("📢 Highlights")
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
######### Inicio price_comparator App
def price_comparator():
    def calculate_unit_price(price, quantity):
        return price / quantity if quantity != 0 else float('inf')
    
    
    st.set_page_config(page_title="Supermarket Price Comparator", page_icon="🛒", layout="centered")
    
    st.title("🛒 Supermarket Price Comparator")
    st.subheader("Quickly check which product is cheaper per unit!")
    
    st.markdown("---")
    
    st.header("🔍 Product 1")
    price1 = st.number_input("Price (R$)", min_value=0.0, value=10.0, step=0.01, key="price1")
    quantity1 = st.number_input("Quantity (kg, L, units...)", min_value=0.01, value=1.0, step=0.1, key="quantity1")
    
    st.markdown("---")
    
    st.header("🔍 Product 2")
    price2 = st.number_input("Price (R$)", min_value=0.0, value=8.0, step=0.01, key="price2")
    quantity2 = st.number_input("Quantity (kg, L, units...)", min_value=0.01, value=0.8, step=0.1, key="quantity2")
    
    st.markdown("---")
    
    if st.button("🚀 Compare Now"):
        unit_price1 = calculate_unit_price(price1, quantity1)
        unit_price2 = calculate_unit_price(price2, quantity2)
    
        st.subheader("💡 Result")
    
        st.write(f"🔸 Product 1 unit price: **R$ {unit_price1:.2f}**")
        st.write(f"🔸 Product 2 unit price: **R$ {unit_price2:.2f}**")
    
        if unit_price1 < unit_price2:
            st.success("✅ **Product 1 is more cost-effective!**")
        elif unit_price2 < unit_price1:
            st.success("✅ **Product 2 is more cost-effective!**")
        else:
            st.info("⚖️ **Both products have the same unit price.**")
    
    st.markdown("---")
    st.caption("Tip: Quantity can be in kg, liters, units, packs, etc.")
######### Fim de price_comparator App
######### Inicio App Puxa Assunto
def Puxa_Conversa():
    st.set_page_config(page_title="💬 Puxa-Conversa", page_icon="💡", layout="wide")
    
    # Inicializar session state
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
    if 'categoria' not in st.session_state:
        st.session_state.categoria = 'profundas'
    if 'perguntas_shuffled' not in st.session_state:
        st.session_state.perguntas_shuffled = {}
    
    # Perguntas por categoria
    perguntas_profundas = [
        "Você acredita em destino ou coincidência?",
        "O que você aprendeu com o seu maior erro?",
        "Se pudesse apagar uma memória, qual seria?",
        "O que você faria se soubesse que não pode fracassar?",
        "Se pudesse fazer uma pergunta ao universo e receber a resposta, qual seria?",
        "O que você gostaria que as pessoas lembrassem sobre você?",
        "Qual é o seu maior medo em relação ao futuro?",
        "Se você pudesse ter uma conversa com seu eu do passado, o que diria?",
        "O que significa sucesso para você?",
        "Qual momento da sua vida te transformou completamente?"
    ]
    
    perguntas_normais = [
    "Sem citar um familiar, qual foi a pessoa mais santa que você já conheceu?",
    "Qual a maior invenção da humanidade desde que você nasceu?",
    "Qual foi a coisa que você teve a chance de aprender, mas acabou deixando de lado?",
    "Quem é a pessoa mais inteligente que você conhece?",
    "Quem é seu maior ídolo no esporte?",
    "Qual é a coisa mais idiota que você já disse?",
    "Quem você gostaria que fosse seu melhor amigo ou sua melhor amiga?",
    "Qual filme já fez você chorar? Por quê?",
    "Qual foi o livro mais marcante da sua vida?",
    "Que qualidade você mais aprecia em um amigo ou amiga?",
    "Você acha que vale a pena ser honesto(a) em todas as ocasiões?",
    "Como você descreveria a si mesmo(a) em apenas cinco palavras?",
    "Sua personalidade tem mais a ver com um gato ou com um cachorro?",
    "Com qual pessoa famosa você mais se parece?",
    "Qual é o tipo de programa de TV que você mais gosta?",
    "Que tipo de filme mais define seu estilo de vida atual: romântico, ação, aventura, suspense, comédia, drama, ficção ou terror?",
    "Se você pudesse comer apenas cinco tipos de comida pelo resto da vida, quais seriam?",
    "Qual é o filme que você mais assistiu repetidas vezes na vida?",
    "Você gostaria de fazer uma tatuagem? Por quê?",
    "Qual foi a pessoa mais famosa com quem você já conversou?",
    "Você acha que ter muitos amigos nas redes sociais é algo bom? Por quê?",
    "Como você interpreta seus sonhos: usa a intuição ou procura significados em livros ou na internet?",
    "Você acha que, para alguém ser considerado bonito(a), é necessário ser magro(a)?",
    "Você ainda guarda algum brinquedo da sua infância? Qual é e por quê?",
    "De que pessoa você tem medo?",
    "Se pudesse ter apenas um superpoder do Superman, qual escolheria?",
    "Se fosse possível saber a idade em que você vai morrer, você gostaria de saber?",
    "Você tem algum ritual matinal ou noturno? Qual?",
    "Qual é a pessoa que mais influencia seu modo de vestir?",
    "Qual é o momento mais importante do seu dia?",
    "Se pudesse ser presidente do Brasil, qual seria sua primeira medida?",
    "Você já passou por uma situação embaraçosa por causa de um comportamento inadequado de um(a) namorado(a) ou cônjuge?",
    "Você acharia correto uma lei que permitisse a um homem ter duas mulheres, ou uma mulher ter dois maridos, ou até mais?",
    "O que faz de você um(a) grande profissional?",
    "Qual é o maior cantor ou cantora do Brasil de todos os tempos?",
    "Qual é a parte mais bonita do seu corpo?",
    "É melhor ser pai/mãe ou ser filho/filha?",
    "Qual é sua loja favorita?",
    "Você acha que os amigos são mais importantes do que a família?",
    "Em uma escala de 1 a 10, qual é a importância da moda na sua vida?",
    "Qual é o esporte mais idiota que você conhece?",
    "Qual foi o momento da vida em que você mais sentiu medo?",
    "Qual foi a compra da qual você mais se arrependeu?",
    "Você acha que a pena de morte é uma boa solução para a violência? Por quê?",
    "Se pudesse ser muito famoso(a) em uma dessas áreas, qual escolheria: música, cinema ou esporte?",
    "Se tivesse que escolher uma parte do seu corpo para colocar no seguro, qual seria?",
    "Que país você não tem a mínima vontade de conhecer? Por quê?",
    "Se fosse obrigado(a) a participar de um reality show, qual escolheria?",
    "O que deixa você mais desconfortável: o frio ou o calor?",
    "Você acha que, quando se trata de um casal, os opostos se atraem ou se repelem?",
    "Com exceção do pai e da mãe, qual foi a pessoa que mais influenciou sua vida?",
    "Qual foi o filme de terror mais assustador que você já viu?",
    "O que mais facilmente afeta seu nível de felicidade?",
    "Qual é a droga — legal ou ilegal — mais perigosa, na sua opinião?",
    "Você se importa com o que os outros pensam de você?",
    "Já pensou em trocar de nome? Por quê? E qual seria?",
    "Se pudesse apagar um ano da sua vida, qual seria? Por quê?",
    "O que mais influencia você: aquilo que você vê ou aquilo que você lê?",
    "Se pudesse ficar invisível agora e xeretar a vida de alguém, quem seria?",
    "É mais fácil você se abrir com os outros ou os outros se abrirem com você?",
    "Qual é o presente que você gostaria de ganhar agora?",
    "Se você soubesse que o mundo iria acabar em seis meses, e tivesse como provar, você avisaria a população?",
    "Quem você acha que foi o brasileiro ou brasileira que mais influenciou os destinos do país?",
    "Qual é o animal que mais fascina você? E qual mais lhe dá medo?",
    "Você já chorou de alegria? Qual foi a situação?",
    "Se você pudesse fazer as outras pessoas acreditarem em algo que você acredita, o que seria?",
    "Que pessoa famosa você considera menos confiável?",
    "Algumas pessoas gostam de falar sobre coisas, outras gostam de fazer coisas. Qual desses dois tipos você é?",
    "O que lhe causa mais raiva?",
    "Qual foi a situação mais embaraçosa que você já viveu por conta de uma mentira?",
    "Você acha que a publicidade influencia muito sua vida? Você costuma comprar produtos que viu em anúncios ou comerciais?",
    "Se pudesse presenciar a conversa entre duas pessoas atuais, quem seriam elas?",
    "O que você faz que mais irrita as pessoas?",
    "Qual foi o apelido mais interessante que já lhe deram? E o pior?",
    "Qual é a comida mais marcante da sua infância?",
    "Quais são os sinais que indicam que você está apaixonado(a)?",
    "O que é mais difícil para você: perdoar ou pedir perdão?",
    "Se você pudesse ser Deus por um dia para realizar um único ato em favor do mundo, o que faria?",
    "Você prefere receber elogios pelas suas realizações ou pelo seu caráter?",
    "Qual foi a maior demonstração de amizade que você já recebeu?",
    "Na sua opinião, por que tantos casais se separam?",
    "Você acha que as novelas prejudicam a formação das crianças?",
    "De que música considerada ridícula por seus amigos (ou pela maioria das pessoas) você gosta?",
    "O que seria mais difícil: passar uma semana sem tomar banho (mas podendo trocar de roupa) ou uma semana sem trocar de roupa (mas podendo tomar banho)?",
    "Você já se apaixonou à primeira vista?",
    "Você concordaria em viver cinco anos a menos se isso fizesse você mais bonito(a) e sensual agora?",
    "Com quem você trocaria de vida por apenas um dia?",
    "Se você pudesse praticar um esporte radical com garantia de que não correria riscos, qual escolheria?",
    "Qual é o melhor lugar da sua casa?",
    "Que tipo de livro você gostaria de escrever: um romance, sua biografia, contos, poesia, autoajuda ou outro gênero? Por quê?",
    "O que os motoristas fazem no trânsito que mais irrita você?",
    "Você acha que os sites de busca estão diminuindo a capacidade de pensar do ser humano?",
    "Qual é o seu super-herói favorito? Por quê?",
    "Se tivesse que escolher apenas uma qualidade pela qual gostaria de ser lembrado(a), qual seria?",
    "Qual foi o maior orgulho que você já deu aos seus pais?",
    "Se pudesse fazer uma viagem no tempo, escolheria o passado ou o futuro?",
    "Qual é o maior grupo musical de todos os tempos, na sua opinião?",
    "Qual foi a melhor série de TV que você já assistiu?",
    "Qual é a coisa mais injusta da vida?",
    "Qual é a profissão que você jamais gostaria de exercer?"
]
    
    # Header
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3rem; margin-bottom: 0.5rem; background: linear-gradient(45deg, #FF6B6B, #4ECDC4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>💬 Puxa-Conversa</h1>
        <p style='color: #666; font-size: 1.1rem;'>Navegue pelas perguntas!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Category Toggle
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        categoria_nova = st.selectbox(
            "Escolha a categoria:",
            options=['profundas', 'normais'],
            format_func=lambda x: f"🧠 Profundas" if x == 'profundas' else f"🎈 Normais",
            index=0 if st.session_state.categoria == 'profundas' else 1,
            key='categoria_select'
        )
        
        # Reset index se mudou categoria
        if categoria_nova != st.session_state.categoria:
            st.session_state.categoria = categoria_nova
            st.session_state.current_index = 0
    
    # Embaralhar perguntas se necessário
    perguntas = perguntas_profundas if st.session_state.categoria == 'profundas' else perguntas_normais
    
    if st.session_state.categoria not in st.session_state.perguntas_shuffled:
        shuffled = perguntas.copy()
        random.shuffle(shuffled)
        st.session_state.perguntas_shuffled[st.session_state.categoria] = shuffled
    
    perguntas_atual = st.session_state.perguntas_shuffled[st.session_state.categoria]
    
    # Funções de navegação
    def next_card():
        st.session_state.current_index = (st.session_state.current_index + 1) % len(perguntas_atual)
    
    def prev_card():
        st.session_state.current_index = (st.session_state.current_index - 1) % len(perguntas_atual)
    
    def reset_cards():
        st.session_state.current_index = 0
        # Re-embaralhar
        shuffled = perguntas.copy()
        random.shuffle(shuffled)
        st.session_state.perguntas_shuffled[st.session_state.categoria] = shuffled
    
    # Card principal
    pergunta_atual = perguntas_atual[st.session_state.current_index]
    proxima_pergunta = perguntas_atual[(st.session_state.current_index + 1) % len(perguntas_atual)]
    
    # CSS para o card estilo Tinder
    st.markdown("""
    <style>
    .tinder-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem 0;
        min-height: 400px;
    }
    
    .card-stack {
        position: relative;
        width: 350px;
        height: 400px;
        perspective: 1000px;
    }
    
    .card {
        position: absolute;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #ffffff, #f8fafc);
        border-radius: 24px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1), 0 6px 12px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
    }
    
    .card-main {
        z-index: 2;
        transform: translateZ(0);
    }
    
    .card-main:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0,0,0,0.15), 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .card-background {
        z-index: 1;
        transform: scale(0.95) translateY(20px);
        opacity: 0.7;
        background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
    }
    
    .card-text {
        font-size: 1.4rem;
        font-weight: 600;
        color: #1e293b;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    .card-counter {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 500;
    }
    
    .controls-container {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 2rem;
        flex-wrap: wrap;
    }
    
    .tinder-btn {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        border: none;
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .tinder-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
    .btn-dislike {
        background: linear-gradient(135deg, #ef4444, #dc2626);
    }
    
    .btn-like {
        background: linear-gradient(135deg, #10b981, #059669);
    }
    
    .btn-back {
        background: linear-gradient(135deg, #6b7280, #4b5563);
        width: 50px;
        height: 50px;
    }
    
    .btn-reset {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        width: 50px;
        height: 50px;
    }
    
    .instructions {
        text-align: center;
        color: #64748b;
        margin-top: 1.5rem;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    @media (max-width: 768px) {
        .card-stack {
            width: 320px;
            height: 380px;
        }
        .card {
            padding: 1.5rem;
        }
        .card-text {
            font-size: 1.2rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display do card
    st.markdown(f"""
<div class="tinder-container">
    <div class="card-stack">
        <div class="card card-main">
            <div>
                <div class="card-text">
                    {pergunta_atual}
                </div>
                <div class="card-counter">
                    {st.session_state.current_index + 1} de {len(perguntas_atual)}
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
    
    # Controles principais
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("↶ Voltar", key="back_btn", help="Pergunta anterior", use_container_width=True):
            prev_card()
            st.rerun()
    
    with col2:
        if st.button("➡️ Próxima", key="next_btn", help="Próxima pergunta", use_container_width=True):
            next_card()
            st.rerun()
    
    with col3:
        if st.button("↻ Resetar", key="reset_btn", help="Resetar e embaralhar", use_container_width=True):
            reset_cards()
            st.rerun()
    
    # Instruções
    st.markdown("""
    <div class="instructions">
        <p><strong>Como navegar:</strong></p>
        <p>👆 <strong>Clique no ícone 📱</strong> acima do card para avançar</p>
        <p>↶ Voltar • ↻ Resetar e embaralhar</p>
    </div>
    """, unsafe_allow_html=True)
######### Fim app puxa assunto

page_names_to_funcs = {
    "My Portfolio": portfolio_app,
    "Retirement App": retirement_app,
    "Puxa Conversa":Puxa_Conversa,
    "Stocks App": stock_dashboard,
    "Price Comparator App": price_comparator
    
}
st.set_page_config(page_title="P. Frey's Creative Showcase", page_icon=':computer:',layout='wide')
selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
