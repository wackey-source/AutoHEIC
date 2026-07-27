import time

from pillow_heif import register_heif_opener

from modules.config import load_config
from modules.log_manager import logger
from modules.watcher import (
    create_observer,
    convert_existing_files,
)

try:
    from modules.tray import start_tray
except Exception:
    start_tray = None


def main():
    register_heif_opener()

    config = load_config()

    watch_folder = config["watch_folder"]
    quality = config.get("quality", 90)
    delete_original = config.get("delete_original", True)
    convert_existing = config.get("convert_existing", True)
    max_width = config.get("max_width", 0)
    max_file_size_kb = config.get("max_file_size_kb", 0)

    logger.info("AutoHEIC avviato")

    if start_tray:
        start_tray()

    if convert_existing:
        convert_existing_files(
            watch_folder,
            quality,
            delete_original,
            max_width,
            max_file_size_kb,
        )

    observer = create_observer(
        watch_folder,
        quality,
        delete_original,
        max_width,
        max_file_size_kb,
    )

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Arresto richiesto")
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()
