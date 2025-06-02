import logging
import re
import urllib.parse

import requests

from src.config import settings

logger = logging.getLogger(__name__)


class MetricService:
    @classmethod
    def __normalize_event_name(cls, event_name):
        # Удаляем эмодзи и спецсимволы (кроме дефиса и пробелов)
        cleaned = re.sub(r"[^\w\s-]", "", str(event_name))

        # Заменяем пробелы и подчеркивания на дефисы
        normalized = re.sub(r"[\s_]+", "-", cleaned.strip())

        # Удаляем повторяющиеся дефисы
        normalized = re.sub(r"-+", "-", normalized)

        # Переводим в lowercase (по желанию)
        return normalized.lower()

    @classmethod
    def send_event(cls, user_id, event_name):
        if not settings.METRIC_COUNTER_ID:
            return
        url = f"https://mc.yandex.ru/watch/{settings.METRIC_COUNTER_ID}"

        safe_event_name = cls.__normalize_event_name(event_name)

        headers = {
            "User-Agent": "Mozilla/5.0 (TelegramBot)",
        }
        params = {
            "page-url": f"https://example.com/{safe_event_name}",
            "t": "gdpr(14)",
            "browser-info": f"ar:1:u:{user_id}",
        }

        # URL-кодируем параметры
        encoded_params = urllib.parse.urlencode(params, safe="", quote_via=urllib.parse.quote)

        try:
            response = requests.get(url, params=encoded_params, headers=headers)
            if response.status_code != 200:
                logger.error(response.status_code, response.text)
        except Exception as ex:
            logger.error(ex)
