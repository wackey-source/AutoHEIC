import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from modules.converter import convert
from modules.log_manager import logger


def wait_complete(file_path: Path, timeout: int = 30):
    """
    Attende che il file abbia terminato la copia.
    """

    previous_size = -1

    for _ in range(timeout):

        try:
            size = file_path.stat().st_size
        except FileNotFoundError:
            return False

        if size == previous_size:
            return True

        previous_size = size
        time.sleep(1)

    return False


class HEICHandler(FileSystemEventHandler):

    def __init__(self, quality, delete_original, max_width):
        self.quality = quality
        self.delete_original = delete_original
        self.max_width = max_width

    def on_created(self, event):

        if event.is_directory:
            return

        file_path = Path(event.src_path)

        if file_path.suffix.lower() != ".heic":
            return

        logger.info(f"Nuovo file rilevato: {file_path.name}")

        if not wait_complete(file_path):
            logger.warning(f"Timeout durante la copia: {file_path.name}")
            return

        convert(
            file_path,
            quality=self.quality,
            delete_original=self.delete_original,
            max_width=self.max_width,
        )


def convert_existing_files(
    folder,
    quality,
    delete_original,
    max_width,
):

    folder = Path(folder)

    logger.info("Controllo file HEIC già presenti...")

    files = sorted(folder.glob("*.heic"))

    if not files:
        logger.info("Nessun file HEIC trovato.")
        return

    logger.info(f"Trovati {len(files)} file HEIC.")

    for file in files:

        convert(
            file,
            quality=quality,
            delete_original=delete_original,
            max_width=max_width,
        )


def create_observer(
    folder,
    quality,
    delete_original,
    max_width,
):

    observer = Observer()

    observer.schedule(
        HEICHandler(
            quality,
            delete_original,
            max_width,
        ),
        folder,
        recursive=False,
    )

    return observer
