import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from modules.converter import convert
from modules.log_manager import logger


converted_files = set()


def wait_complete(file_path, timeout=30):
    previous_size = -1
    stable_count = 0
    start = time.time()

    while time.time() - start < timeout:
        try:
            current_size = os.path.getsize(file_path)
        except OSError:
            return False

        if current_size == previous_size and current_size > 0:
            stable_count += 1
            if stable_count >= 2:
                return True
        else:
            stable_count = 0

        previous_size = current_size
        time.sleep(1)

    return False


def process_file(file_path, quality, delete_original, max_width):
    file_path = os.path.abspath(file_path)

    if not file_path.lower().endswith(".heic"):
        return

    if file_path in converted_files:
        return

    logger.info(f"Rilevato file: {os.path.basename(file_path)}")

    if not wait_complete(file_path):
        logger.warning(f"File non ancora completo: {file_path}")
        return

    if convert(file_path, quality, delete_original, max_width):
        converted_files.add(file_path)


class HEICHandler(FileSystemEventHandler):

    def __init__(self, quality, delete_original, max_width):
        self.quality = quality
        self.delete_original = delete_original
        self.max_width = max_width

    def on_created(self, event):
        if not event.is_directory:
            process_file(
                event.src_path,
                self.quality,
                self.delete_original,
                self.max_width,
            )

    def on_modified(self, event):
        if not event.is_directory:
            process_file(
                event.src_path,
                self.quality,
                self.delete_original,
                self.max_width,
            )


def convert_existing_files(folder, quality, delete_original, max_width):
    logger.info("Controllo file HEIC già presenti...")

    found = False

    for filename in os.listdir(folder):
        if filename.lower().endswith(".heic"):
            found = True
            file_path = os.path.join(folder, filename)

            if convert(file_path, quality, delete_original, max_width):
                converted_files.add(os.path.abspath(file_path))

    if not found:
        logger.info("Nessun file HEIC trovato.")


def create_observer(folder, quality, delete_original, max_width):
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

    logger.info(f"Monitoraggio cartella: {folder}")

    return observer
