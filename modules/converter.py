from pathlib import Path

from PIL import Image

from modules.log_manager import logger


def convert(
    file_path: Path,
    quality: int = 95,
    delete_original: bool = True,
    max_width: int = 0,
) -> bool:
    """
    Converte un file HEIC in JPG.

    Returns:
        True se la conversione è riuscita.
        False in caso di errore.
    """

    try:

        file_path = Path(file_path)

        output_file = file_path.with_suffix(".jpg")

        logger.info(f"Conversione: {file_path.name}")

        with Image.open(file_path) as image:

            image = image.convert("RGB")

            if max_width > 0 and image.width > max_width:

                ratio = max_width / image.width
                new_height = int(image.height * ratio)

                image = image.resize(
                    (max_width, new_height),
                    Image.LANCZOS,
                )

            image.save(
                output_file,
                "JPEG",
                quality=quality,
                optimize=True,
            )

        logger.info(f"Creato: {output_file.name}")

        if delete_original:
            file_path.unlink(missing_ok=True)
            logger.info(f"Eliminato: {file_path.name}")

        return True

    except Exception as exc:

        logger.exception(
            f"Errore durante la conversione di {file_path}: {exc}"
        )

        return False
