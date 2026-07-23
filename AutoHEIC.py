import json
import os
import time
from pathlib import Path

from PIL import Image
from pillow_heif import register_heif_opener
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

register_heif_opener()

# -------------------------
# Configurazione
# -------------------------

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "watch_folder": str(Path.home() / "Downloads"),
    "output_format": "JPEG",
    "delete_original": True,
    "quality": 95,
}


def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG

    with open(CONFIG_FILE) as f:
        return json.load(f)


cfg = load_config()

watch_folder = cfg["watch_folder"]
output_format = cfg["output_format"].upper()
delete_original = cfg["delete_original"]
quality = cfg["quality"]
MAX_WIDTH = 2048


# -------------------------
# Conversione
# -------------------------

def convert(path):

    try:

        print(f"Conversione: {os.path.basename(path)}")

        img = Image.open(path)

        # Ridimensiona se troppo grande
        MAX_WIDTH = 2048

        if img.width > MAX_WIDTH:
            ratio = MAX_WIDTH / img.width
            new_height = int(img.height * ratio)
            img = img.resize(
                (MAX_WIDTH, new_height),
                Image.Resampling.LANCZOS
            )

        output = os.path.splitext(path)[0] + ".jpg"

        # Non sovrascrivere un JPG già esistente
        if os.path.exists(output):
            print("JPG già presente, conversione saltata.")
            return

        img.convert("RGB").save(
            output,
            "JPEG",
            quality=85,
            optimize=True
        )

        print("Creato:", output)

        if delete_original:
            os.remove(path)
            print("HEIC eliminato")

    except Exception as e:

        print("Errore:", e)


# -------------------------
# Attende copia completata
# -------------------------

def wait_complete(file):

    size = -1

    while True:

        try:
            new = os.path.getsize(file)
        except:
            return False

        if new == size:
            return True

        size = new
        time.sleep(1)


# -------------------------
# Watchdog
# -------------------------

class Handler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        if not event.src_path.lower().endswith(".heic"):
            return

        print("Nuovo file:", event.src_path)

        if wait_complete(event.src_path):
            convert(event.src_path)


observer = Observer()

observer.schedule(
    Handler(),
    watch_folder,
    recursive=False,
)

observer.start()

print("--------------------------------------")
print(" AutoHEIC")
print("--------------------------------------")
print("Monitoraggio:", watch_folder)
print()

try:

    while True:
        time.sleep(1)

except KeyboardInterrupt:

    observer.stop()

observer.join()
