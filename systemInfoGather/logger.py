import logging


def get_logger(name, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    FORMAT = "[%(asctime)s: %(filename)s - line %(lineno)s - %(funcName)5s() ] %(message)s"
    formater = logging.Formatter(FORMAT)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formater)
    logger.addHandler(console_handler)
    return logger
