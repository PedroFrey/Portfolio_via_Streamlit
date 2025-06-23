
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

## Dashboard Assets
urllib.request.urlretrieve('https://raw.githubusercontent.com/PedroFrey/Portfolio_via_Streamlit/refs/heads/master/cash-management-dashboard.png', "cash-management-dashboard.png")
img_finacial = Image.open('cash-management-dashboard.png')

urllib.request.urlretrieve('https://raw.githubusercontent.com/PedroFrey/Portfolio_via_Streamlit/refs/heads/master/pmo.png', "pmo.png")
img_pmo = Image.open('pmo.png')

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

# Encapsulate stock app
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
# encapsulate the entire portfolio
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
      st.markdown("[Explore PMO Dashboard for Project Insights](https://www.google.com)")
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

# Função de simulação
def simular_aposentadoria(params, inicio=date.today().strftime("%Y-%m-%d"), eventos_extraordinarios=None):
    r_mensal = (1 + params["retorno_real_anual"])**(1/12) - 1
    meses_ate_aposentar = (params["idade_aposentadoria"] - params["idade_atual"]) * 12
    meses_apos_aposentar = (params["expectativa_vida"] - params["idade_aposentadoria"]) * 12
    total_meses = meses_ate_aposentar + meses_apos_aposentar

    capital_necessario = params["valor_desejado_por_ano"] / params["taxa_retirada_anual"]

    if params["aporte_mensal"] is None:
        aporte = capital_necessario * r_mensal / ((1 + r_mensal)**meses_ate_aposentar - 1)
    else:
        aporte = params["aporte_mensal"]

    retirada_mensal = params["valor_desejado_por_ano"] / 12

    datas = pd.date_range(start=inicio, periods=total_meses, freq='MS')
    df = pd.DataFrame(index=range(total_meses))
    df["data"] = datas
    df["ano"] = df["data"].dt.year
    df["mes_nome"] = df["data"].dt.strftime("%b/%Y")

    eventos_dict = {}
    if eventos_extraordinarios:
        for evento in eventos_extraordinarios:
            data_evento = pd.to_datetime(evento["data"]).replace(day=1)
            eventos_dict[data_evento] = eventos_dict.get(data_evento, 0) + evento["valor"]

    patrimonio = params.get("patrimonio", 0)
    patrimonio_lista = []
    aporte_lista = []
    retirada_lista = []
    fase_lista = []

    for mes in range(total_meses):
        data_mes = datas[mes]
        fase = "Crescimento" if mes < meses_ate_aposentar else "Aposentadoria"

        patrimonio *= (1 + r_mensal)

        if fase == "Crescimento":
            patrimonio += aporte
            aporte_lista.append(aporte)
            retirada_lista.append(0)
        else:
            patrimonio -= retirada_mensal
            retirada_lista.append(retirada_mensal)
            aporte_lista.append(0)

        if data_mes in eventos_dict:
            patrimonio += eventos_dict[data_mes]

        patrimonio = max(patrimonio, 0)
        patrimonio_lista.append(patrimonio)
        fase_lista.append(fase)

    df["patrimonio"] = patrimonio_lista
    df["aporte"] = aporte_lista
    df["retirada"] = retirada_lista
    df["fase"] = fase_lista
    df["aporte_mensal"] = aporte
    df["retirada_mensal"] = retirada_mensal
    df["capital_necessario"] = capital_necessario

    return df


# Função retirement_app
def retirement_app():
    st.title("💰 Simulador de Aposentadoria")

    st.sidebar.header("🧠 Dados do Usuário")

    idade_atual = st.sidebar.number_input("Idade atual", min_value=0, max_value=120, value=18, step=1)

    idade_aposentadoria = st.sidebar.number_input("Idade para aposentadoria", min_value=idade_atual, max_value=120, value=65, step=1)

    expectativa_vida = st.sidebar.number_input("Expectativa de vida", min_value=idade_aposentadoria, max_value=150, value=85, step=1)

    valor_desejado_por_ano = st.sidebar.number_input("Renda desejada na aposentadoria (por mês)", min_value=0, value=1_500, step=100)*12

    retorno_real_anual = st.sidebar.number_input("Rentabilidade real anual (%)", min_value=0.0, max_value=1.0, value=0.04, step=0.01)

    aporte_mensal = st.sidebar.number_input("Aporte mensal até aposentadoria", min_value=0, value=300, step=100)

    patrimonio_inicial = st.sidebar.number_input("Patrimônio inicial", min_value=0, value=0_000, step=500)

    st.sidebar.markdown("---")
    st.sidebar.subheader("📅 Eventos extraordinários")
    evento1_data = st.sidebar.date_input("Data do evento", value=date(2035, 12, 1))
    evento1_valor = st.sidebar.number_input("Valor do evento", value=0, step=1000)

    eventos = [{"data": evento1_data.strftime('%Y-%m-%d'), "valor": evento1_valor}] if evento1_valor != 0 else []

    params = {
        "idade_atual": idade_atual,
        "idade_aposentadoria": idade_aposentadoria,
        "expectativa_vida": expectativa_vida,
        "valor_desejado_por_ano": valor_desejado_por_ano,
        "taxa_retirada_anual": 1.0,
        "retorno_real_anual": retorno_real_anual,
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
    ax.set_xticklabels(df["mes_nome"][::12], rotation=45)

    ax.set_xlabel("Mês/Ano")
    ax.set_ylabel("Patrimônio acumulado")
    ax.set_title("Evolução do Patrimônio")
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

    st.subheader("📈 Evolução dos dados")
    st.dataframe(df_formatado[["data", "patrimonio", "fase", "aporte", "retirada"]].set_index("data"))
# fim app aposentadoria


page_names_to_funcs = {
    "My Portfolio": portfolio_app,
    "Stocks App": stock_dashboard,
    "Retirement App": retirement_app
}
st.set_page_config(page_title="P. Frey's Creative Showcase", page_icon=':computer:',layout='wide')
selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
