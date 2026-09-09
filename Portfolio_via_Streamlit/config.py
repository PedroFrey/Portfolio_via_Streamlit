"""Configuracao central do app.

Usa pydantic-settings para validar e tipar env vars / secrets, com falha
explicita e legivel na inicializacao em vez de erros silenciosos espalhados
pelo codigo (o problema do antigo ``os.environ.get`` + print de warning).

Valores podem vir de (em ordem de precedencia): variaveis de ambiente reais
(Render), ``.streamlit/secrets.toml`` (lido via st.secrets e injetado como
env var no boot), ou um ``.env`` local para desenvolvimento.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
LOTTIES_DIR = ASSETS_DIR / "lotties"
QUESTIONS_DIR = ASSETS_DIR / "questions"
WEB_ELEMENTS_DIR = ASSETS_DIR / "WebDevElements"


class Settings(BaseSettings):
    """Configuracao de ambiente, validada e tipada.

    Nenhum campo aqui e obrigatorio: o app deve degradar graciosamente
    (ex: sem SENTRY_DSN, so nao reporta erros; sem PHONE_NUMBER, so nao
    manda notificacao) em vez de quebrar no boot.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: Literal["development", "production"] = "production"
    log_level: str = "INFO"

    phone_number: str | None = Field(default=None, alias="PHONE_NUMBER")
    call_me_bot_api_key: str | None = Field(default=None, alias="CALL_ME_BOT_API_KEY")

    sentry_dsn: str | None = Field(default=None, alias="SENTRY_DSN")

    posthog_api_key: str | None = Field(default=None, alias="POSTHOG_API_KEY")
    posthog_host: str = Field(default="https://us.i.posthog.com", alias="POSTHOG_HOST")

    @property
    def notifications_enabled(self) -> bool:
        return bool(self.phone_number and self.call_me_bot_api_key)

    @property
    def sentry_enabled(self) -> bool:
        return bool(self.sentry_dsn)

    @property
    def analytics_enabled(self) -> bool:
        return bool(self.posthog_api_key)


def _load_streamlit_secrets_into_env() -> None:
    """Espelha st.secrets para os.environ, se um secrets.toml existir."""
    try:
        import streamlit as st

        for key, value in st.secrets.items():
            if isinstance(value, str) and key not in os.environ:
                os.environ[key] = value
    except Exception:  # nosec B110 — fallback intencional: sem secrets.toml (ex: testes/CI)
        pass


_load_streamlit_secrets_into_env()
settings = Settings()
