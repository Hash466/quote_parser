import json
import re

import aiofiles

from core.config import result_file
from core.logger import get_logger

logger = get_logger(__name__)


def text_clean(text: str) -> str:
    logger.debug("Очищаю текст от лишних символов")
    cleaned_text = re.sub(r'\s+', ' ', text).strip()
    return cleaned_text


async def save_json_async(data: dict, filename: str = result_file):
    logger.debug("Формирую данные для сохранения в файл в формате json")

    json_data = json.dumps(data, indent=4)
    
    logger.debug("Сохраняю собранные данные в файл %s", filename)
    async with aiofiles.open(filename, "w") as file:
        await file.write(json_data)
