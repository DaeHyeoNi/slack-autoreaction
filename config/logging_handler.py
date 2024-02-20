import logging

_logger: logging.Logger = logging.getLogger(__name__)

formatter = logging.Formatter("[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s")

streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
_logger.addHandler(streamHandler)

_logger.setLevel(level=logging.INFO)


def get_logger():
    return _logger
