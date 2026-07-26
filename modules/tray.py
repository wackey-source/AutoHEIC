import os
import platform
import threading

import pystray
from PIL import Image, ImageDraw
from pystray import MenuItem as Item

from modules.app_state import get_config
from modules.log_manager import logger
from modules.watcher import convert_existing_files


def create_icon():
    image = Image.new("RGB", (64, 64), "white")
    draw = ImageDraw.Draw(image)

    draw.rectangle((8, 8, 56, 56), fill="#4CAF50", outline="black")
    draw.rectangle((18, 18, 46, 46), fill="white")

    return image


def open_downloads():
    if platform.system() == "Windows":
        os.startfile(os.path.expanduser("~/Downloads"))


def open_log():
    if platform.system() == "Windows":
        os.startfile(os.path.abspath("logs/autoheic.log"))


def convert_now():
    cfg = get_config()

    if not cfg:
        logger.warning("Configurazione non disponibile.")
        return

    logger.info("Conversione manuale richiesta dalla tray.")

    convert_existing_files(
        cfg["watch_folder"],
        cfg["quality"],
        cfg["delete_original"],
        cfg["max_width"],
    )


def exit_app(icon):
    logger.info("Chiusura richiesta dalla tray.")
    icon.stop()
    os._exit(0)


def start_tray():

    menu = pystray.Menu(
        Item("Apri Downloads", lambda icon, item: open_downloads()),
        Item("Apri log", lambda icon, item: open_log()),
        Item("Converti file esistenti", lambda icon, item: convert_now()),
        pystray.Menu.SEPARATOR,
        Item("Esci", lambda icon, item: exit_app(icon)),
    )

    icon = pystray.Icon(
        "AutoHEIC",
        create_icon(),
        "AutoHEIC",
        menu,
    )

    threading.Thread(target=icon.run, daemon=True).start()
