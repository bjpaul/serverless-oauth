import logging

from common.config import Config

common = Config()

logging.basicConfig(format='%(levelname)s : %(asctime)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

logger = logging.getLogger(common.app_name)
level = logging.getLevelName(common.log_level)
logger.setLevel(level)


def message_builder(message):
    return "App name : " + common.app_name + " : Message Id : " + common.request_id + " > " + str(message)


def debug(message):
    logger.debug(message_builder(message))


def info(message):
    logger.info(message_builder(message))


def warn(message):
    logger.warning(message_builder(message))


def error(message):
    logger.error(message_builder(message))
