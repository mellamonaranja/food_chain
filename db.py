import sqlalchemy
from sqlalchemy import create_engine
from typing import Optional
from utils import get_logger
logger = get_logger("db")


def get_engine(
        driver: str,
        user_name: str,
        user_password: str,
        db_host: str,
        db_port: str,
        db_name: str,
        **kwargs) -> Optional[sqlalchemy.engine.Engine]:
    """
    인자값을 전달하여 sqlalchemy engine 인스턴스를 받음
    :param driver:
    :param user_name:
    :param user_password:
    :param db_host:
    :param db_port:
    :param db_name:
    :param kwargs:
    :return:Union[sqlalchemy.engine, None]
    """
    url = f"{driver}://{user_name}:{user_password}@{db_host}:{db_port}/{db_name}"
    logger.info(f"get_engine {url}")
    try:
        return get_engine_with_url(url, **kwargs)
    except Exception as e:
        logger.error(e)
        return None


def get_engine_with_url(db_url: str, **kwargs) -> sqlalchemy.engine.Engine:
    """
    db_url 및 kwargs를 입력 받아 sqlalchemy engine 인스턴스를 받음
    :param db_url:
    :param kwargs:
    :return: sqlalchemy.engine
    """
    logger.info(f"get_engine_with_url {db_url}")
    return create_engine(db_url, **kwargs)



