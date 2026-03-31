import os
from pathlib import Path
from dotenv import load_dotenv


# Diretório raiz do projeto (um nível acima da pasta 'config')
PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]

load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

# Minhas credenciais do Spotify
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
BASE_URL = "https://api.spotify.com/v1"
TOKEN_ACCESS = os.getenv("SPOTIFY_TOKEN_ACCESS")
# Controle de verificação SSL para ambientes corporativos com certificado auto-assinado.
# Valores aceitos: 'true' (padrão), 'false', '0', 'no', 'none' ou caminho para CA bundle.
raw_verify = os.getenv("SPOTIFY_REQUESTS_VERIFY", "true").strip().lower()
if raw_verify in ("false", "0", "no", "none"):
    REQUESTS_VERIFY = False
else:
    REQUESTS_VERIFY = raw_verify  # True / caminho de CA bundle / 'true'

# Remova os prints ao colocar em produção
print(CLIENT_ID)
print(CLIENT_SECRET)
print(TOKEN_ACCESS)