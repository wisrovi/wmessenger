"""
Crea las credenciales del bot de Telegram en el vault de WAuth.

Ejecuta este script una sola vez para configurar el token del bot
y los usuarios autorizados.
"""

from wauth import WAuth

# Custom database path (debe ser el mismo que usa el receiver)
DB_PATH = "./my_secrets.db"

auth = WAuth(db_path=DB_PATH)






# ── Token del bot ──────────────────────────────────────────────
TELEGRAM_TOKEN = "8657603474:AAGinzBWeU5BgBIMJ2T3BhwAvrAbCQHz80w"

# ── Usuarios autorizados (IDs numéricos) ───────────────────────
# Tu ID numérico: escríbele a @userinfobot en Telegram

TELEGRAM_CHAT_ID = "6586101740"

AUTHORIZED_USERS = [TELEGRAM_CHAT_ID]  # ← Reemplaza con tu(s) ID(s)

# Guardar en el vault
auth.set("telegram_token", TELEGRAM_TOKEN)
auth.set("authorized_users", ",".join(AUTHORIZED_USERS))

print("✅ Credenciales guardadas en:", DB_PATH)
print(f"   Token: {TELEGRAM_TOKEN[:10]}...")
print(f"   Usuarios autorizados: {AUTHORIZED_USERS}")
