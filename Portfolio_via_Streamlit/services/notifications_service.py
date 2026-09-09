"""Notificacao via WhatsApp (CallMeBot), com retry e logging estruturado.

Antes: chamada disparada como efeito colateral no import do modulo da pagina.
Agora e uma funcao pura de I/O, chamada explicitamente pela pagina com um
guard de ``st.session_state`` para disparar no maximo uma vez por sessao.
"""

from __future__ import annotations

from urllib.parse import quote

import requests
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from Portfolio_via_Streamlit.config import settings
from Portfolio_via_Streamlit.logging_config import get_logger

log = get_logger(__name__)

_CALLMEBOT_URL = "https://api.callmebot.com/whatsapp.php"


@retry(
    reraise=False,
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
    retry=retry_if_exception_type(requests.RequestException),
)
def _send(url: str) -> requests.Response:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response


def send_whatsapp_message(message: str) -> bool:
    """Envia mensagem via CallMeBot WhatsApp. Retorna True se enviou com sucesso.

    Nunca lanca excecao: notificacao e best-effort e nao pode derrubar a
    pagina. Falhas sao logadas de forma estruturada.
    """
    if not settings.notifications_enabled:
        log.info("whatsapp_notification_skipped", reason="not_configured")
        return False

    url = (
        f"{_CALLMEBOT_URL}?phone={settings.phone_number}"
        f"&text={quote(message)}&apikey={settings.call_me_bot_api_key}"
    )
    try:
        _send(url)
    except requests.RequestException as exc:
        log.error("whatsapp_notification_failed", error=str(exc))
        return False
    else:
        log.info("whatsapp_notification_sent")
        return True
