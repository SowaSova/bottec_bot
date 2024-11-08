# core/logger.py
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from core.config import settings


def setup_logging():
    """
    Настройка логирования: вывод в консоль и запись в файл с ротацией.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Форматтер для логов
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Обработчик для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Убедимся, что директория для логов существует
    log_dir = Path(settings.LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)

    # Обработчик для записи в файл с ротацией
    file_handler = RotatingFileHandler(
        filename=log_dir / settings.LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 МБ
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Логгер готов к использованию
    logger.info("Логирование настроено успешно.")
