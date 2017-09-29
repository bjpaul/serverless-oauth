import logging

from common.config import Config

common = Config()
logging.basicConfig(format='%(levelname)s : %(asctime)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(common.app_name)

class Log(object):
    def __init__(self):
        level = logging.getLevelName(common.log_level)
        logger.setLevel(level)

    def message_builder(self, message):
        return "App name : " + common.app_name + " : Message Id : " + common.request_id + " > " + str(message)

    def debug(self, message):
        logger.debug(self.message_builder(message))

    def info(self, message):
        logger.info(self.message_builder(message))

    def warn(self, message):
        logger.warning(self.message_builder(message))

    def error(self, message):
        logger.error(self.message_builder(message))
