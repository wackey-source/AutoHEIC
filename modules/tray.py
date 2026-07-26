import os
import threading

import pystray
from PIL import Image, ImageDraw
from pystray import MenuItem as Item

from modules.log_manager import logger


def _create_icon():
    """Crea un'icona semplice (quadrato verde con bordo nero)."""
    image = Image.new("RGB", (64, 64), "white")
    draw = ImageDraw.Draw(image)

    draw.rectangle((8, 8, 56, 56), fill="green", outline="black")
    draw.rectangle((18, 18, 46, 46), fill="white")

    return image


def _exit(icon):
    logger.info("Chiusura richiesta dalla tray.")
    icon.stop()
    os._exit(0)


def start_tray():
    icon = pystray.Icon(
        "AutoHEIC",
        _create_icon(),
        "AutoHEIC",
        menu=pystray.Menu(
            Item("Esci", lambda icon, item: _exit(icon)),
        ),
    )

    threading.Thread(target=icon.run, daemon=True).start()
