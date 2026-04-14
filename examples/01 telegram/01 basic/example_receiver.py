"""
Ejemplo: Receiver de Telegram Bot

Requiere que primero ejecutes example_create_config.py para
configurar el token del bot en el vault.
"""

from wauth import WAuth

from wconnect import WMessage, Wtelegram

# ── Vault con las credenciales ────────────────────────────────
DB_PATH = "./my_secrets.db"  # Mismo path que example_create_config.py
my_vault = WAuth(db_path=DB_PATH)

# ── Inicializar Telegram con auth ─────────────────────────────
tg = Wtelegram(auth_instance=my_vault)

# Leer usuarios autorizados del vault (si existen)
authorized_users_raw = getattr(my_vault, "get", lambda k: None)("authorized_users") or ""
AUTHORIZED_USERS = [u.strip() for u in authorized_users_raw.split(",") if u.strip()]


# 1. Recibir un comando específico
@tg.command(command="status")
def get_status(message: WMessage):
    user = message.username
    texto = message.text

    print(f"Comando status recibido de: {message.chat_id}")
    print(f"El usuario {user} envió: {texto}")
    tg.send(to=message.chat_id, message=f"Hola {user}, el sistema está OK ✅")


# 2. Recibir cualquier mensaje de texto (Consumer general)
@tg.consumer(value_type="text")
def handle_all_text(message: WMessage):
    print(f"Mensaje general de {message.username}: {message.text}")


# 3. Recibir fotos
@tg.consumer(value_type="image")
def handle_images(message: WMessage):
    # message.file es un objeto WFile
    print(f"Imagen recibida de {message.username}")
    # Podemos descargarla directamente
    message.file.save(f"./downloads/{message.file.name}")
    print(f"Imagen guardada como {message.file.name}")


# 4. Recibir documentos (CSVs, ZIPs, etc.)
@tg.consumer(value_type="document")
def handle_files(message: WMessage):
    print(f"Archivo recibido: {message.file.name}")

    # Procesamiento Green-IT: Leer sin guardar en disco
    data = message.file.content  # Obtiene los bytes directamente
    print(f"Tamaño del archivo: {len(data)} bytes")

    if message.file.name.endswith(".csv"):
        print("Procesando CSV para wclickhouse...")


@tg.consumer(value_type="image")
def handle_authorized_images(message: WMessage):
    # Solo permiten mi propio ID (o una lista de autorizados)
    if AUTHORIZED_USERS and message.user_id not in AUTHORIZED_USERS:
        tg.send(
            to=message.chat_id, message="🚫 No tienes permiso para enviar imágenes."
        )
        return

    print(f"Imagen recibida de usuario autorizado: {message.username}")
    message.file.save(f"./vault/{message.file.name}")


# Solo reacciona si el mensaje viene de este usuario específico
@tg.consumer(value_type="image", from_user="12345678")
def handle_my_images(message: WMessage):
    print("He recibido una imagen de mi dueño.")


tg.run_bot()
