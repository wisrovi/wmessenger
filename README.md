# wconnect (wmessenger)

`wconnect` (`wmessenger`) es una librería en Python diseñada para simplificar la creación de bots e integración con plataformas de mensajería (Telegram). Ofrece abstracciones orientadas a objetos, soporte para el protocolo Context Manager (`with`), descarga automática de archivos adjuntos (`auto_save_in`), y decoradores intuitivos compatibles con la convención de `wkafka` y `wredis`.

---

## 🛠️ Tecnologías y Librerías Relevantes

Este componente utiliza las siguientes tecnologías y librerías clave de su ecosistema:

- **[python-telegram-bot](https://python-telegram-bot.org/)**: Cliente asíncrono para interactuar con la Telegram Bot API y gestionar la infraestructura de handlers y polling/webhooks.
- **[wauth](https://pypi.org/project/wauth/)**: Librería del ecosistema para almacenamiento seguro y encriptado de credenciales, tokens y lista de usuarios autorizados.
- **[requests](https://requests.readthedocs.io/)**: Cliente HTTP síncrono para envíos directos y descarga de archivos binarios desde Telegram CDN.
- **[aiohttp](https://docs.aiohttp.org/)**: Motor HTTP asíncrono para operaciones I/O sin bloqueo.

---

## 📦 Instalación

```bash
pip install wconnect
```

---

## 🔐 Métodos de Autenticación

`wconnect` soporta 3 formas flexibles para inicializar el cliente `Wtelegram`:

### 1. Vía WAuth Vault (Base de Datos Encriptada)
```python
from wauth import WAuth
from wconnect import Wtelegram

vault = WAuth(db_path="./my_secrets.db")
bot = Wtelegram(auth_instance=vault)
```

### 2. Vía Token Directo
```python
from wconnect import Wtelegram

bot = Wtelegram(token="8823336064:AAE2sky0B4vOD5_z2cKsDekv4T9LSKiSlGA")
```

### 3. Vía Variable de Entorno (`TELEGRAM_BOT_TOKEN`)
```bash
export TELEGRAM_BOT_TOKEN="8823336064:AAE2sky0B4vOD5_z2cKsDekv4T9LSKiSlGA"
```
```python
from wconnect import Wtelegram

bot = Wtelegram()  # Detecta automáticamente TELEGRAM_BOT_TOKEN
```

---

## 📥 Recepción de Mensajes (Receiver)

Permite registrar escuchadores mediante decoradores como `@bot.on_command(...)` y `@bot.on_message(...)` o `@bot.consumer(...)`.

### Ejemplo con Descarga Automática (`auto_save_in` y `saved_path`)

```python
from wconnect import WMessage, Wtelegram

# auto_save_in descarga imágenes y documentos en ./downloads sin código adicional
bot = Wtelegram(token="YOUR_BOT_TOKEN", auto_save_in="./downloads")


@bot.on_command(command="status")
def handle_status(message: WMessage) -> None:
    bot.send(to=message.chat_id, message="Servicio Online ✅")


@bot.on_message(value_type="image")
def handle_image(message: WMessage) -> None:
    print(f"Imagen guardada automáticamente en: {message.saved_path}")


@bot.on_message(value_type="document")
def handle_document(message: WMessage) -> None:
    print(f"Archivo guardado automáticamente en: {message.saved_path}")


# Mismo estándar de consumo que wkafka / wredis
bot.run_consumers(block=True)
```

---

## 📤 Envío de Contenido (Sender)

Soporta envíos de texto, imágenes (auto-detectando si es URL o archivo local) y documentos utilizando el protocolo Context Manager (`with`):

```python
from wconnect import WFile, Wtelegram

with Wtelegram(token="YOUR_BOT_TOKEN") as producer:
    # 1. Mensaje de Texto
    producer.send(to="CHAT_ID", message="✅ Operación completada")

    # 2. Imagen desde URL o Ruta Local
    producer.send_image(
        to="CHAT_ID",
        url="https://httpbin.org/image/png",
        caption="Gráfico Analytics",
    )

    # 3. Documento en memoria (WFile) o desde disco
    data_bytes = b"id,value\n1,100"
    doc_file = WFile(content=data_bytes, name="report.csv")
    producer.send_document(to="CHAT_ID", file=doc_file)
```

---

## 📁 Estructura de Ejemplos

Puedes consultar ejemplos listos para ejecutar en la carpeta `examples/01 telegram/`:

- **`00 config/`**: Formas de inicialización (Vault, Token Directo, Env Var).
- **`01 receiver/`**: Casos de uso de recepción (`01 text`, `02 image`, `03 document`, `04 command`, `05 all`).
- **`02 sender/`**: Casos de uso de envío (`01 text`, `02 image`, `03 document`).

---

## 📄 Licencia
MIT License - Copyright (c) 2025 William Rodriguez