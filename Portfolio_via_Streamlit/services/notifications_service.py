# services/notifications_service.py
import os
import requests
from urllib.parse import quote

PHONE_NUMBER = os.environ.get("PHONE_NUMBER")
CALL_ME_BOT_API_KEY = os.environ.get("CALL_ME_BOT_API_KEY")

def send_whatsapp_message(message: str):
    """
    Envia mensagem via CallMeBot WhatsApp
    """
    if not PHONE_NUMBER or not CALL_ME_BOT_API_KEY:
        print("⚠️ Variáveis de ambiente não definidas")
        return False

    url = f"https://api.callmebot.com/whatsapp.php?phone={PHONE_NUMBER}&text={quote(message)}&apikey={CALL_ME_BOT_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("✅ Mensagem enviada com sucesso!")
        return True
    except requests.RequestException as e:
        print(f"❌ Erro ao enviar mensagem: {e}")
        return False


# --- Bloco para teste no terminal ---
if __name__ == "__main__":
    send_whatsapp_message("Teste do notifications_service.py")