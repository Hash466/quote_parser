import re
import json
import aiofiles

from core.config import result_file
from core.logger import get_logger


logger = get_logger(__name__)


def text_clean(text: str) -> str:
    logger.debug("Очищаю текст от лишних символов")
    # decoded_text = text.encode().decode("unicode_escape")
    decoded_text = text.encode('utf-8').decode('unicode_escape').encode('latin1').decode('utf-8')
    cleaned_text = re.sub(r'\s+', ' ', decoded_text).strip()
    return cleaned_text


async def save_json_async(data: dict, filename: str = result_file):
    logger.debug("Формирую данные для сохранения в файл в формате json")
    print("~~~>>> ", data)
    json_data = json.dumps(data, indent=4)
    
    logger.debug("Сохраняю собранные данные в файл %s", filename)
    async with aiofiles.open(filename, "w") as file:
        await file.write(json_data)
