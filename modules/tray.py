import os
import sys
import platform
import threading

import pystray
from PIL import Image
from pystray import MenuItem as Item

from modules.app_state import get_config
from modules.log_manager import logger
from modules.watcher import convert_existing_files


def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(__file__))

    return os.path.join(base_path, relative_path)


ICON_PATH = resource_path("icons/autoheic.ico")


def load_icon():
    return Image.open(ICON_PATH)


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
    icon = pystray.Icon(
        "AutoHEIC",
        load_icon(),
        "AutoHEIC",
        menu=pystray.Menu(
            Item("Apri Downloads", lambda icon, item: open_downloads()),
            Item("Apri log", lambda icon, item: open_log()),
            Item("Converti file esistenti", lambda icon, item: convert_now()),
            pystray.Menu.SEPARATOR,
            Item("Esci", lambda icon, item: exit_app(icon)),
        ),
    )

    threading.Thread(target=icon.run, daemon=True).start()
