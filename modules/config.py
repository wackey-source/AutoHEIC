import json
import os
from pathlib import Path

CONFIG_FILE = Path("config.json")

DEFAULT_CONFIG = {
    "watch_folder": str(Path.home() / "Downloads"),
    "delete_original": True,
    "quality": 95,
    "max_width": 0,
    "convert_existing": True,
}


def save_config(config: dict):
    """Salva il file di configurazione."""
    with CONFIG_FILE.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


def load_config() -> dict:
    """
    Carica config.json.
    Se non esiste lo crea automaticamente.
    Aggiunge automaticamente eventuali nuove chiavi.
    """

    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    with CONFIG_FILE.open("r", encoding="utf-8") as f:
        config = json.load(f)

    modified = False

    for key, value in DEFAULT_CONFIG.items():
        if key not in config:
            config[key] = value
            modified = True

    if modified:
        save_config(config)

    config["watch_folder"] = os.path.expandvars(
        os.path.expanduser(config["watch_folder"])
    )

    return config
