import logging
from pathlib import Path

def init(name: str = "etl", level: int = logging.INFO) -> logging.Logger:
    """
    Конфигурирует логгер проекта.

    :param name: название логгера 
    :param level: минимальный уровень сообщений
    :return: настроенный logger
    """
    logs_dir = Path(__file__).resolve().parents[1] / "logs"
    logs_dir.mkdir(exist_ok=True)

    log_file = logs_dir / "pipeline.log"

    # формат сообщений
    fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

    logging.basicConfig(
        level=level,
        format=fmt,
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()          # чтобы всё ещё видеть вывод в консоли
        ],
    )
    return logging.getLogger(name)
