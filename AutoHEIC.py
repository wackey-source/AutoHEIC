import time
import platform

from modules.tray import start_tray
from modules.app_state import set_config

from pillow_heif import register_heif_opener

from modules.config import load_config
from modules.log_manager import logger
from modules.watcher import (
    convert_existing_files,
    create_observer,
)

def main():

    register_heif_opener()

    logger.info("========== Avvio AutoHEIC ==========")

    cfg = load_config()
    set_config(cfg)

if platform.system() == "Windows":
    start_tray()

    watch_folder = cfg["watch_folder"]
    delete_original = cfg["delete_original"]
    quality = cfg["quality"]
    max_width = cfg["max_width"]
    convert_existing = cfg["convert_existing"]

    if convert_existing:
        convert_existing_files(
            watch_folder,
            quality,
            delete_original,
            max_width,
        )

    observer = create_observer(
        watch_folder,
        quality,
        delete_original,
        max_width,
    )

    observer.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Arresto richiesto dall'utente.")

    finally:
        observer.stop()
        observer.join()
        logger.info("AutoHEIC terminato.")


if __name__ == "__main__":
    main()
