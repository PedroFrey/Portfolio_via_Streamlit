# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

## [0.2.0] — Refatoramento completo

### Adicionado
- Camada `domain/` com logica pura de simulacao de aposentadoria (Pydantic
  models, sem I/O) — testavel isoladamente e com property-based testing.
- Observabilidade: logging estruturado (structlog/JSON), error boundary por
  pagina (`@safe_page`), correlacao por `session_id`, integracao opcional
  com Sentry e PostHog.
- `config.py` com `pydantic-settings`.
- Pagina inicial (`Home`) com catalogo dos mini-apps.
- Navegacao nativa via `st.navigation`/`st.Page`.
- Filtros lazy no simulador de aposentadoria (`st.form` + botao "Aplicar"),
  com valores padrao ja calculados na primeira carga.
- Grafico interativo (Plotly) no lugar do Matplotlib estatico.
- Formatacao monetaria via `babel` no lugar de `.replace()` manual.
- Retry com backoff (`tenacity`) nas chamadas HTTP de notificacao.
- Testes: `pytest` + `hypothesis` para o dominio, `AppTest` para smoke test
  de cada pagina, mocks para o servico de notificacao.
- CI (GitHub Actions): lint, type-check, testes com cobertura, bandit,
  pip-audit. Dependabot para dependencias e Actions.
- `.pre-commit-config.yaml`, `Dockerfile`, tema centralizado em
  `.streamlit/config.toml`.

### Corrigido
- `st.set_page_config` estava duplicado dentro de paginas individuais —
  agora centralizado em `app.py`.
- Notificacao via WhatsApp era disparada como efeito colateral no import do
  modulo — agora e chamada explicita, com guard de uma notificacao por
  sessao.
- Chaves de `session_state` sem namespace podiam colidir entre paginas —
  prefixadas por pagina.
- Parametros do simulador trafegavam como `dict` solto por string, sem
  validacao — causa raiz de um bug real no codigo legado (`app_old.py`
  referenciava uma chave inexistente).

### Removido
- `app_old.py` (codigo morto duplicado).
- `.config/` (arquivos de gcloud commitados por engano).
- `__pycache__/` commitado.
- Divergencia entre `pyproject.toml` (Poetry) e `requirements.txt` (pip
  freeze) — unificado em `uv`.

## [0.1.0] — Estado anterior ao refactor
Ver historico do Git anterior a esta tag.
