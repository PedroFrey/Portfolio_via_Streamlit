import requests
import os
import sys

# Adiciona a pasta do pacote ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Portfolio_via_Streamlit.config import LOTTIES_DIR

# Cria a pasta caso não exista
os.makedirs(LOTTIES_DIR, exist_ok=True)

# URLs dos Lotties
lottie_urls = {
    "what_do_i_do": "https://assets3.lottiefiles.com/packages/lf20_5tl1xxnz.json",
    "server": "https://assets2.lottiefiles.com/packages/lf20_rrqimc3f.json"
}

# Baixar e salvar localmente
for name, url in lottie_urls.items():
    r = requests.get(url)
    if r.status_code == 200:
        path = os.path.join(LOTTIES_DIR, f"{name}.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write(r.text)
    else:
        print(f"Falha ao baixar {name}: {r.status_code}")