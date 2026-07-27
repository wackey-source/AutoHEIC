from pathlib import Path
import io

from PIL import Image

from modules.log_manager import logger


def save_jpeg_target_size(
    image,
    output_file,
    quality,
    max_file_size_kb,
):
    """
    Salva il JPEG cercando automaticamente la qualità migliore
    per rimanere sotto la dimensione desiderata.
    """

    # Se non è impostato alcun limite usa il comportamento classico
    if max_file_size_kb <= 0:
        image.save(
            output_file,
            "JPEG",
            quality=quality,
            optimize=True,
            progressive=True,
        )
        return quality, output_file.stat().st_size // 1024

    min_quality = 40
    max_quality = quality

    best_bytes = None
    best_quality = min_quality

    while min_quality <= max_quality:

        current_quality = (min_quality + max_quality) // 2

        buffer = io.BytesIO()

        image.save(
            buffer,
            "JPEG",
            quality=current_quality,
            optimize=True,
            progressive=True,
        )

        size_kb = len(buffer.getvalue()) / 1024

        if size_kb <= max_file_size_kb:
            best_bytes = buffer.getvalue()
            best_quality = current_quality
            min_quality = current_quality + 1
        else:
            max_quality = current_quality - 1

    if best_bytes is None:
        buffer = io.BytesIO()

        image.save(
            buffer,
            "JPEG",
            quality=40,
            optimize=True,
            progressive=True,
        )

        best_bytes = buffer.getvalue()
        best_quality = 40

    with open(output_file, "wb") as f:
        f.write(best_bytes)

    return best_quality, len(best_bytes) // 1024


def convert(
    file_path: Path,
    quality: int = 90,
    delete_original: bool = True,
    max_width: int = 0,
    max_file_size_kb: int = 0,
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

            used_quality, final_size = save_jpeg_target_size(
                image,
                output_file,
                quality,
                max_file_size_kb,
            )

        logger.info(
            f"Creato: {output_file.name} "
            f"({final_size} KB, qualità {used_quality})"
        )

        if delete_original:
            file_path.unlink(missing_ok=True)
            logger.info(f"Eliminato: {file_path.name}")

        return True

    except Exception as exc:

        logger.exception(
            f"Errore durante la conversione di {file_path}: {exc}"
        )

        return False
