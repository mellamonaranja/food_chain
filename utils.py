import warnings
import logging
from logging.handlers import RotatingFileHandler
from logging import StreamHandler
warnings.filterwarnings(action="ignore")
from pathlib import Path


def get_root() -> str:
    return Path(__file__).parent.parent

def get_logger(job_name: str) -> logging.Logger:
    """
    logger를 생성.
    :param job_name:
    :return: loggger 인스턴스
    """
    log_max_size = 10 * 512 * 1024
    log_file_count = 5
    logger = logging.getLogger(job_name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = True

    formatter = logging.Formatter("%(asctime)s;[%(levelname)s];%(message)s",
                                              "%Y-%m-%d %H:%M:%S")
    log_dir = Path(f"{get_root()}/item_recommend/log/")
    if not log_dir.exists():
        log_dir.mkdir()

    file_handler = RotatingFileHandler(filename=f"{get_root()}/item_recommend/log/log.txt",
                                        maxBytes=log_max_size,
                                        backupCount=log_file_count)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    stream_handler = StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger
