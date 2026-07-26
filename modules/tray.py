import os
import platform
import subprocess
import threading

import pystray
from PIL import Image, ImageDraw
from pystray import MenuItem as Item

from modules.log_manager import logger


def create_icon():
    image = Image.new("RGB", (64, 64), "white")
    draw = ImageDraw.Draw(image)

    draw.rectangle((8, 8, 56, 56), fill="#4CAF50", outline="black")
    draw.rectangle((18, 18, 46, 46), fill="white")

    return image


def open_downloads():
    path = os.path.expanduser("~/Downloads")

    if platform.system() == "Windows":
        os.startfile(path)


def open_log():
    log_file = os.path.abspath("logs/autoheic.log")

    if platform.system() == "Windows":
        os.startfile(log_file)


def convert_now():
    logger.info("Conversione manuale richiesta dalla tray.")


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
