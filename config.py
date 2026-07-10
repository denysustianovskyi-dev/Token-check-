import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Опційно: ключі GoPlus для вищих рейт-лімітів (не обов'язково для старту)
GOPLUS_APP_KEY = os.getenv("GOPLUS_APP_KEY", "")
GOPLUS_APP_SECRET = os.getenv("GOPLUS_APP_SECRET", "")

# Chain ID для мереж, які підтримує GoPlus Security API
# Повний список: https://docs.gopluslabs.io/reference/chain-id
CHAINS = {
    "eth": "1",
    "bsc": "56",
    "polygon": "137",
    "arbitrum": "42161",
    "base": "8453",
}
DEFAULT_CHAIN = "eth"
