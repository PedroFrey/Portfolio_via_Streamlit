
def carregar_perguntas(categoria):
    caminho = f"Portfolio_via_Streamlit/assets/questions/questions_{categoria}.txt"
    with open(caminho, "r", encoding="utf-8") as f:
        perguntas = [linha.strip() for linha in f if linha.strip()]
    return perguntas

# --- Bloco para teste no terminal ---
if __name__ == "__main__":
    carregar_perguntas("profundas")