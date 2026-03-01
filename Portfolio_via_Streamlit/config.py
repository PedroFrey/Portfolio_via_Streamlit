import os

# Base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Pastas de assets
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
LOTTIES_DIR = os.path.join(ASSETS_DIR, "lotties")

# Variáveis de ambiente
PHONE_NUMBER = os.environ.get("PHONE_NUMBER")
CALL_ME_BOT_API_KEY = os.environ.get("CALL_ME_BOT_API_KEY")