# wmessenger (wconnect)

`wmessenger` (paquete `wconnect`) es una librería en Python para la integración rápida y elegante con servicios de mensajería (Telegram). Proporciona abstracciones limpias mediante decoradores para recibir comandos, texto, imágenes y archivos, además de gestionar envíos y context managers.

## Tecnologías y Librerías Relevantes

Este componente utiliza las siguientes tecnologías y librerías clave de su ecosistema:

- **[python-telegram-bot](https://python-telegram-bot.org/)**: Cliente asíncrono principal para interactuar con la API de Bots de Telegram.
- **[wauth](https://pypi.org/project/wauth/)**: Librería para almacenamiento seguro y encriptado de credenciales y tokens.
- **[requests](https://requests.readthedocs.io/)**: Cliente HTTP síncrono utilizado para envíos directos a la Telegram Bot API.
- **[aiohttp](https://docs.aiohttp.org/)**: Soporte asíncrono HTTP.

## Instalación

```bash
pip install wconnect
```

## Uso Básico

```python
from wconnect import Wtelegram, WMessage

tg = Wtelegram(token="YOUR_TELEGRAM_BOT_TOKEN")

@tg.command(command="start")
def start_handler(message: WMessage):
    tg.send(to=message.chat_id, message="¡Hola desde Wtelegram!")

tg.run_bot()
```