import time

from pillow_heif import register_heif_opener

from config import load_config
from log_manager import logger
from watcher import (
    convert_existing_files,
    create_observer,
)

register_heif_opener()

logger.info("========== Avvio AutoHEIC ==========")


def main():

    cfg = load_config()

    watch_folder = cfg["watch_folder"]
    delete_original = cfg["delete_original"]
    quality = cfg["quality"]
    convert_existing = cfg["convert_existing"]
    max_width = cfg["max_width"]

    if convert_existing:

        convert_existing_files(
            watch_folder,
            delete_original,
            quality,
            max_width,
        )

    observer = create_observer(
        watch_folder,
        delete_original,
        quality,
        max_width,
    )

    observer.start()

    print("--------------------------------------")
    print(" AutoHEIC")
    print("--------------------------------------")
    print("Monitoraggio:", watch_folder)
    print()

    logger.info(
        f"Monitoraggio avviato: {watch_folder}"
    )

    try:

        while True:

            time.sleep(1)

    except KeyboardInterrupt:

        logger.info(
            "Chiusura richiesta dall'utente"
        )

        observer.stop()

    observer.join()

    logger.info(
        "AutoHEIC terminato"
    )


if __name__ == "__main__":

    main()
