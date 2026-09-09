"""Testes do servico de notificacao — sem chamadas de rede reais."""

from __future__ import annotations

from unittest.mock import patch

import requests

from Portfolio_via_Streamlit.services.notifications_service import send_whatsapp_message


def test_retorna_false_quando_nao_configurado() -> None:
    with patch("Portfolio_via_Streamlit.services.notifications_service.settings") as mock_settings:
        mock_settings.notifications_enabled = False
        assert send_whatsapp_message("teste") is False


def test_retorna_true_em_caso_de_sucesso() -> None:
    with patch("Portfolio_via_Streamlit.services.notifications_service.settings") as mock_settings:
        mock_settings.notifications_enabled = True
        mock_settings.phone_number = "5511999999999"
        mock_settings.call_me_bot_api_key = "fake-key"

        with patch("Portfolio_via_Streamlit.services.notifications_service._send") as mock_send:
            mock_send.return_value.status_code = 200
            assert send_whatsapp_message("teste") is True


def test_retorna_false_em_caso_de_falha_de_rede() -> None:
    with patch("Portfolio_via_Streamlit.services.notifications_service.settings") as mock_settings:
        mock_settings.notifications_enabled = True
        mock_settings.phone_number = "5511999999999"
        mock_settings.call_me_bot_api_key = "fake-key"

        with patch(
            "Portfolio_via_Streamlit.services.notifications_service._send",
            side_effect=requests.RequestException("timeout"),
        ):
            assert send_whatsapp_message("teste") is False
