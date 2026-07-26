import os

from PIL import Image

from log_manager import logger


def convert(path, delete_original=True, quality=85, max_width=2048):
    """
    Converte un file HEIC in JPG.

    Args:
        path (str): Percorso del file HEIC.
        delete_original (bool): Elimina l'HEIC dopo la conversione.
        quality (int): Qualità JPEG.
        max_width (int): Larghezza massima dell'immagine.
    """

    try:

        filename = os.path.basename(path)

        logger.info(f"Conversione: {filename}")

        img = Image.open(path)

        if img.width > max_width:

            ratio = max_width / img.width

            new_height = int(img.height * ratio)

            img = img.resize(
                (max_width, new_height),
                Image.Resampling.LANCZOS
            )

            logger.info(
                f"Immagine ridimensionata a {max_width}px"
            )

        output = os.path.splitext(path)[0] + ".jpg"

        if os.path.exists(output):

            logger.info(
                f"JPG già presente: {os.path.basename(output)}"
            )

            return False

        img.convert("RGB").save(
            output,
            "JPEG",
            quality=quality,
            optimize=True
        )

        logger.info(
            f"Creato: {os.path.basename(output)}"
        )

        if delete_original:

            os.remove(path)

            logger.info(
                f"HEIC eliminato: {filename}"
            )

        return True

    except Exception:

        logger.exception(
            f"Errore durante la conversione di {path}"
        )

        return False
