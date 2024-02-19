import logging

logger: logging.Logger = logging.getLogger(__name__)

formatter = logging.Formatter("[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s")

streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

logger.setLevel(level=logging.INFO)
