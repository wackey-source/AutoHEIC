import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from converter import convert
from log_manager import logger


def wait_complete(file):

    size = -1

    while True:

        try:
            new = os.path.getsize(file)

        except OSError:
            return False

        if new == size:
            return True

        size = new

        time.sleep(1)


class Handler(FileSystemEventHandler):

    def __init__(
        self,
        delete_original,
        quality,
        max_width,
    ):

        self.delete_original = delete_original
        self.quality = quality
        self.max_width = max_width

    def on_created(self, event):

        if event.is_directory:
            return

        if not event.src_path.lower().endswith(".heic"):
            return

        logger.info(
            f"Nuovo file: {event.src_path}"
        )

        if wait_complete(event.src_path):

            convert(
                event.src_path,
                delete_original=self.delete_original,
                quality=self.quality,
                max_width=self.max_width,
            )


def convert_existing_files(
    watch_folder,
    delete_original,
    quality,
    max_width,
):

    logger.info(
        "Controllo file HEIC già presenti..."
    )

    found = False

    for file in sorted(os.listdir(watch_folder)):

        if not file.lower().endswith(".heic"):
            continue

        found = True

        convert(
            os.path.join(
                watch_folder,
                file,
            ),
            delete_original=delete_original,
            quality=quality,
            max_width=max_width,
        )

    if not found:

        logger.info(
            "Nessun file HEIC trovato."
        )


def create_observer(
    watch_folder,
    delete_original,
    quality,
    max_width,
):

    observer = Observer()

    observer.schedule(
        Handler(
            delete_original,
            quality,
            max_width,
        ),
        watch_folder,
        recursive=False,
    )

    return observer
