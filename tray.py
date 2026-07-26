import os
import pystray

from PIL import Image
from pystray import MenuItem as item


class TrayIcon:

    def __init__(self, stop_callback):

        self.stop_callback = stop_callback

        icon_path = os.path.join(
            os.path.dirname(__file__),
            "icons",
            "autoheic.ico"
        )

        self.icon = pystray.Icon(
            "AutoHEIC",
            Image.open(icon_path),
            "AutoHEIC",
            menu=pystray.Menu(
                item("Esci", self.quit)
            )
        )

    def quit(self, icon, menu_item):
        self.stop_callback()
        self.icon.stop()

    def run(self):
        self.icon.run()
