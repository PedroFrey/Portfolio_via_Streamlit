"""Portfolio_via_Streamlit — portfolio pessoal em Streamlit.

Estrutura:
    domain/        Logica de negocio pura (sem I/O, sem Streamlit) — testavel isoladamente.
    services/      Camada de I/O: notificacoes, assets externos. Chama domain/ quando aplicavel.
    presentation/  Paginas Streamlit (UI). Nao deve conter regra de negocio.
"""

__version__ = "0.2.0"
