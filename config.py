import json
import os
from pathlib import Path

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "watch_folder": str(Path.home() / "Downloads"),
    "output_format": "JPEG",
    "delete_original": True,
    "quality": 85,
    "convert_existing": True,
    "max_width": 2048,
}


def load_config():
    """
    Carica il file config.json.
    Se non esiste, lo crea con i valori di default.
    """

    if not os.path.exists(CONFIG_FILE):

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:

            json.dump(
                DEFAULT_CONFIG,
                f,
                indent=4
            )

        return DEFAULT_CONFIG

    with open(CONFIG_FILE, encoding="utf-8") as f:

        cfg = json.load(f)

    # aggiunge automaticamente le nuove opzioni
    changed = False

    for key, value in DEFAULT_CONFIG.items():

        if key not in cfg:

            cfg[key] = value
            changed = True

    if changed:

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:

            json.dump(
                cfg,
                f,
                indent=4
            )

    return cfg
