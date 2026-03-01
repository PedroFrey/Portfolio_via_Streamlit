import os
import json
from Portfolio_via_Streamlit.config import LOTTIES_DIR

def load_lottie(filename: str):
    """
    Carrega um Lottie JSON local do diretório LOTTIES_DIR.
    Retorna o conteúdo do JSON ou None se não existir.
    """
    path = os.path.join(LOTTIES_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None